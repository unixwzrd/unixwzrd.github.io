# Keep a short link through a source move

This small lab loads an unchanged snapshot of this site's `01_short_link_injector.rb` module and gives it invented post objects. It needs Ruby but no Jekyll install, network access, or copy of the real site's posts.

From the extracted `short-link-lab` directory, run:

```bash
ruby run_lab.rb
```

The runner reports three checks: a fixed `short_link_basis` keeps the same short URL after a simulated source move; without that field, the source-path fallback changes the code; and a declared `short_url` that disagrees with the computed URL is rejected. It also prints the invented short URL so you can compare runs.

The module is the active site's short-link calculation as inspected for Part 4. The runner uses tiny stand-ins for Jekyll post and site objects, so this is a test of the module's decision logic, not a Jekyll build. It does not generate redirect HTML or verify a deployed route. The site's post-build scripts handle generated files, and an operator still has to check public reachability separately.
