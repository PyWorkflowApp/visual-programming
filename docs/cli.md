# Command-line Interface

PyWorkflow is first-and-foremost a visual programming application, designed to
help data scientists and many others build workflows to view, manipulate, and
output their data into new formats. Therefore, all workflows must first be
created via the user-interface and saved for later execution.

However, it may not always be ideal to have the client and server deployed
locally or on a remote server just to run your workflows. Power-users want the
ability to running multiple workflows at once, schedule workflow runs, and
dynamically pass data from workflows via stdin/stdout in traditional shell
scripts. This is where the inclusion of PyWorkflow's CLI really shines.

## Command-line syntax

```
pyworkflow execute workflow-file...
```
### Commands

#### Execute
Accepts one or more workflow files as arguments to execute. PyWorkflow will load
the file(s) specified and output status messages to `stdout`. If a workflow
fails to run because of an exception, these will be logged to `stderr`.

**Single-file example**
```
pyworkflow execute ./workflows/my_workflow.json
```

**Batch processing**

Many shells offer different wildcards that can be used to work with multiple
files on the command line, or in scripts. A useful one is the `*` wildcard that
matches matches anything. Used in the following example, it has the effect of
passing all files located within the `workflows` directory to the `execute`
command. 
 
```
pyworkflow execute ./workflows/*
```

## Using `stdin`/`stdout` to modify workflows

Two powerful tools when writing shell scripts are redirection and pipes, which
allow you to dynamically pass data from one command to another. Using these
tools, you can pass different data in to and out of workflows that define what
standard behavior should occur.

PyWorkflow comes with a Read CSV input node and Write CSV output node. When data
is provided via `stdin` on the command-line, it will modify the workflow 
behavior to redirect the Read CSV node to that data. Similarly, if a destination
is specified for `stdout`, the Write CSV node output will be redirected there.

Input data can be passed to PyWorkflow in a few ways.
1) Redirection
```
# Data from sample_file.csv is passed to a Read CSV node
pyworkflow execute my_workflow.json < sample_file.csv
```
2) Pipes
```
# Two CSV files are combined and passed in to a Read CSV node
cat sample_file.csv more_data.csv | pyworkflow execute my_workflow.json

# Data from a 'csv_exporter' tool is passed to a Read CSV node
csv_exporter generate | pyworkflow execute my_workflow.json
```

Output data can be passed from PyWorkflow in a few ways.
1) Redirection
```
# Output from a Write CSV node is stored in a new file 'output.csv'
pyworkflow execute my_workflow.json > output.csv 
```
2) Pipes 
```
# Output from a Write CSV node is searched for the phrase 'foobar'
pyworkflow execute my_workflow.json | grep "foobar"
```
