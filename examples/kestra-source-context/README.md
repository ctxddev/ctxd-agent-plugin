# Source context with Kestra and ctxd

When a workflow changes a source, the next reader needs that change. This Kestra
flow exercises the handoff with [ctxd](https://ctxd.dev), open-source context
infrastructure between agents and data.

The flow runs one Python task in a disposable Docker container. It:

1. Creates a small release checklist and synchronizes it into ctxd.
2. Reads the checklist through the ctxd Python client.
3. Edits the source and confirms the stored read is unchanged before synchronization.
4. Synchronizes again and checks that the next read contains the edit.
5. Saves the reads and installed ctxd version in `result.json`.

Run it in your own Kestra instance with its Docker task runner enabled. The worker
needs access to Docker, the `python:3.12` image and PyPI. The full Python image
includes the system `ps` command used by ctxd. The task installs the released
package with `pip install ctxd`.

In the Kestra UI, create a flow, paste [flow.yaml](flow.yaml), save and execute it.
The execution should finish as **SUCCESS**. Under the `verify_source_change`
task's outputs, open `result.json`: `passed` should be `true`, and `changed_read`
should include the linter step.

The source and ctxd store live inside the task container. Kestra retains the
result file. This example uses no existing documents, model calls or paid
services. It demonstrates explicit synchronization and bounded reads; it does
not measure synchronization latency or answer quality.

To try this with an agent, start with the [ctxd setup guide](../../README.md).
[Browse or star ctxd](https://github.com/ctxd-dev/ctxd).

Kestra references: [Docker setup](https://kestra.io/docs/installation/docker),
[Python Script task](https://kestra.io/plugins/plugin-script-python/io.kestra.plugin.scripts.python.script).
