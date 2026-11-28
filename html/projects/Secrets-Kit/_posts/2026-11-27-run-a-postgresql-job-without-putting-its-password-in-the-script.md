---
layout: post
title: "Run a PostgreSQL job without putting its password in the script"
date: 2026-11-27 20:30:00 -0600
category: Secrets-Kit
permalink_slug: run-a-postgresql-job-without-putting-its-password-in-the-script
tags: [secrets-management, local-first, developer-tools]
excerpt: "Use the free Secrets Kit client to pass a single PostgreSQL credential to psql at launch, then prove the query fails without it and succeeds with it."
image:
  path: /assets/images/blog/secrets-kit/postgres-job-hero.jpg
  width: 1672
  height: 941
  alt: "Secrets Kit: PostgreSQL jobs without hard-coded passwords."
---

A database job needs a password. The job script doesn't need to carry it. In this walkthrough, we'll use Secrets Kit to pass a single PostgreSQL credential to `psql` at launch. The query is just `SELECT 1;`: enough to prove the connection works, without touching application data.

[Install Secrets Kit]({{ '/projects/Secrets-Kit/get-started/#install-it-yourself' | relative_url }}) if you haven't already. This uses the free local client, tested here with Secrets Kit 2.0.5 and PostgreSQL 17. No agent, peer, or Remote Secret Sync subscription is needed.

## Start with a disposable database role

Use a local test database called `demo_db` and a throwaway login role called `demo_app` that can connect to it. Your local TCP connection must require a password; trust authentication would make this test meaningless. The examples use loopback and port `5432`. If your test server listens on a different port, use the same port in both commands. Secrets Kit stores the credential you give it; it doesn't create or rotate the PostgreSQL role.

## Run the control without a password

Use a fresh Bash shell. This unsets inherited connection overrides for this shell and rules out a password from your normal `.pgpass`. `-X` skips `psql` startup files and `-w` tells the client never to prompt for a password.

```bash
unset PGPASSWORD PGSERVICE PGSERVICEFILE PGHOSTADDR
demo_passfile=$(mktemp "${TMPDIR:-/tmp}/seckit-pgpass.XXXXXX") || exit 1
export PGPASSFILE="$demo_passfile"
trap 'rm -- "$demo_passfile"' EXIT

psql -X -w -h 127.0.0.1 -p 5432 -U demo_app -d demo_db -Atc 'SELECT 1;'
```

Expect `no password supplied`. A connection error means the test server or connection settings need attention; if you get `1`, stop and check the server's authentication settings before going on. `-w` stops an interactive prompt; it doesn't force the server to require a password.

## Store one credential and run the same query

Enter the role's password at the hidden prompt. This keeps it out of command arguments and shell history. The `website-demo` account below is a Secrets Kit label, separate from PostgreSQL's `demo_app` role. Use a fresh demo label if you've already used it for another test.

```bash
set +x
IFS= read -r -s -p 'Disposable PostgreSQL password: ' demo_password
printf '\n'
printf '%s' "$demo_password" | seckit set --service postgres --account website-demo --name PGPASSWORD --stdin
unset demo_password
```

Now run the same connection and query, selecting only the `PGPASSWORD` entry from that service and account:

```bash
seckit run --service postgres --account website-demo --names PGPASSWORD -- \
  psql -X -w -h 127.0.0.1 -p 5432 -U demo_app -d demo_db -Atc 'SELECT 1;'
```

The result should be `1`, followed by a return to the shell. The rest of the job can use the same pattern: leave the non-secret connection arguments and the work in the job, and pass the selected password when the process starts.

{% include blog_diagram.html src="/assets/images/blog/secrets-kit/postgres-job-terminal.svg" alt="Verified terminal output: psql fails with no password supplied; the same query launched through Secrets Kit prints 1." caption="Output from the disposable loopback test, with the connection details and commands shortened to fit." %}

## What this keeps out of your script

The password isn't in the script or `psql` arguments. It **is** in the child process environment, and Secrets Kit passes through the parent environment too. Keep it out of traces, environment dumps, and application logs. [PostgreSQL warns](https://www.postgresql.org/docs/current/libpq-envars.html) that process environments are inspectable on some systems. If your setup requires PostgreSQL's password-file interface, see the [versioned application examples](https://github.com/unixwzrd/Secrets-Kit/blob/v2.0.5/docs/EXAMPLES.md#postgresql-redis-and-batch-applications): selecting a file path is a different workflow and does not encrypt the file itself.

When you're done, close the demo shell and retire the disposable database role and the matching Secrets Kit entry. For more examples, see the [Secrets Kit guides]({{ '/projects/Secrets-Kit/guides/' | relative_url }}). If your next job needs authorized peers across networks, read about [optional Remote Secret Sync]({{ '/projects/Secrets-Kit/remote-sync/' | relative_url }}).

