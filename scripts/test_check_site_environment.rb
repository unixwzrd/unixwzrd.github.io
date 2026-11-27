#!/usr/bin/env ruby
# frozen_string_literal: true

require "minitest/autorun"
require "open3"
require "tmpdir"
require "fileutils"
require "shellwords"

# Isolated fixtures only: no installs, commits, network calls or site builds.
class CheckSiteEnvironmentTest < Minitest::Test
  ROOT = File.expand_path("..", __dir__)

  def setup
    @dir = Dir.mktmpdir("check-site-environment-")
    @bin = File.join(@dir, "bin")
    FileUtils.mkdir_p(File.join(@dir, "utils/bin/checks"))
    FileUtils.mkdir_p(@bin)
    FileUtils.cp(File.join(ROOT, "utils/bin/check_site.sh"), File.join(@dir, "utils/bin/check_site.sh"))
    FileUtils.cp(File.join(ROOT, "utils/bin/checks/01_environment.sh"), File.join(@dir, "utils/bin/checks/01_environment.sh"))
    executable("git", "printf '%s\\n' \"$FIXTURE_ROOT\"")
    executable("bundle", "echo inherited-bundle; exit 0")
    executable("python", "echo inherited-python; exit 0")
    @env = { "HOME" => @dir, "PATH" => "#{@bin}:/usr/bin:/bin", "FIXTURE_ROOT" => @dir, "TMPDIR" => @dir }
    File.write(File.join(@dir, "requirements.txt"), "")
  end

  def teardown
    FileUtils.remove_entry(@dir)
  end

  def executable(name, body, directory = @bin)
    FileUtils.mkdir_p(directory)
    path = File.join(directory, name)
    File.write(path, "#!/bin/bash\n#{body}\n")
    FileUtils.chmod(0o755, path)
    path
  end

  def run_check
    Open3.capture2e(@env, "/bin/bash", "utils/bin/check_site.sh", "--run", "01_environment", chdir: @dir, unsetenv_others: true)
  end

  def test_gui_environment_selects_existing_conda_and_rvm_environments
    ruby_bin = File.join(@dir, "project-ruby/bin")
    executable("bundle", "echo project-bundle; exit 0", ruby_bin)
    FileUtils.mkdir_p(File.join(@dir, ".rvm/environments"))
    File.write(File.join(@dir, ".rvm/environments/ext-ruby-3.3.4@unixwzrd.github.io"), "export PATH=#{Shellwords.escape(ruby_bin)}:\"$PATH\"\n")
    conda_root = File.join(@dir, "miniconda3")
    executable("python", "echo project-conda-python; exit 0", File.join(conda_root, "envs/python-website-dev/bin"))
    FileUtils.mkdir_p(File.join(conda_root, "etc/profile.d"))
    File.write(File.join(conda_root, "etc/profile.d/conda.sh"), 'conda() { export PATH="$2/bin:$PATH"; }' + "\n")
    output, status = run_check
    assert status.success?, output
    assert_includes output, "project-bundle"
    assert_includes output, "project-conda-python"
    refute_includes output, "inherited-bundle"
    refute_includes output, "inherited-python"
  end

  def test_hosts_without_local_environments_keep_the_callers_tools
    output, status = run_check
    assert status.success?, output
    assert_includes output, "inherited-bundle"
    assert_includes output, "inherited-python"
  end

  def test_missing_locked_gems_stop_before_python_checks
    executable("bundle", "echo missing-locked-gem; exit 1")
    output, status = run_check
    refute status.success?, output
    assert_includes output, "missing-locked-gem"
    refute_includes output, "inherited-python"
    refute_includes output, "All checks passed"
  end

  def test_python_failure_is_fatal_and_never_attempts_installation
    executable("python", "echo python-args:\"$*\"; exit 1")
    output, status = run_check
    refute status.success?, output
    assert_includes output, "no packages were installed"
    refute_includes output, "-m pip"
    refute_includes output, "All checks passed"
  end

  def real_python
    candidates = [ENV["CHECK_TEST_PYTHON"], File.join(Dir.home, "miniconda3/envs/python-website-dev/bin/python3"), File.join(Dir.home, "anaconda3/envs/python-website-dev/bin/python3")].compact
    candidates.find { |path| File.executable?(path) } || Open3.capture2("which", "python3").first.strip
  end

  def check_requirements(requirements)
    executable("python", "exec #{Shellwords.escape(real_python)} \"$@\"")
    File.write(File.join(@dir, "requirements.txt"), requirements)
    run_check
  end

  def test_installed_requirements_comments_and_environment_markers
    installed, status = Open3.capture2(real_python, "-c", "from importlib.metadata import version; print(version('packaging'))")
    assert status.success?
    output, status = check_requirements("# comment\npackaging==#{installed.strip} # installed\nmissing-test-package; python_version < '2'\n")
    assert status.success?, output
    assert_includes output, "Python requirements satisfied"
  end

  def test_missing_distribution_is_reported_without_installing
    output, status = check_requirements("dts-nonexistent-check-fixture-package==1\n")
    refute status.success?, output
    assert_includes output, "not installed"
    assert_includes output, "no packages were installed"
  end

  def test_wrong_installed_version_is_rejected
    output, status = check_requirements("packaging==0.0.0\n")
    refute status.success?, output
    assert_includes output, "packaging==0.0.0: installed"
  end

  def test_text_cleanup_preserves_modes_when_replacing_and_restaging_files
    executable("git", <<~BASH)
      case "$*" in
        'diff --name-only --cached') printf '%s\\n' script.sh notes.md ;;
        'diff --name-only'|'diff --cached --name-only') printf '%s\\n' script.sh notes.md ;;
        check-ignore*) exit 1 ;;
        add*) printf '%s\\n' "$*" >> "$FIXTURE_ROOT/restaged" ;;
      esac
    BASH
    executable("cleanup-text", "cat; printf 'cleaned\\n'")
    script = executable("script.sh", "echo fixture", @dir)
    notes = File.join(@dir, "notes.md")
    File.write(notes, "fixture notes\n")
    FileUtils.chmod(0o640, notes)
    original_modes = [script, notes].map { |path| File.stat(path).mode & 0o7777 }
    output, status = Open3.capture2e(@env, "/bin/bash", File.join(ROOT, "utils/bin/checks/13_cleanup_text.sh"), chdir: @dir, unsetenv_others: true)
    assert status.success?, output
    assert_equal original_modes, [script, notes].map { |path| File.stat(path).mode & 0o7777 }
    assert_includes File.read(script), "cleaned"
    assert_includes File.read(notes), "cleaned"
    assert_equal ["add script.sh", "add notes.md"].sort, File.readlines(File.join(@dir, "restaged"), chomp: true).sort
    assert_equal [], Dir.glob(File.join(@dir, "tmp.*"))
  end
end


