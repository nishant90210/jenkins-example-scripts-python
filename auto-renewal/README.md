# automatic-membership-renewal
This folder contains an automated solution for membership renewal using Jenkins pipeline, SCM integration, file uploader, and a Python script.

## Prerequisites

To use this solution, you need to have the following components set up:

1. Jenkins: An instance of Jenkins CI/CD tool to run the pipeline.
2. Python: Install Python on the Jenkins server or agent.
3. Bitbucket: Set up a Bitbucket repository to store the Jenkins file and scripts.

## Setup

1. Clone this repository to your local machine or Jenkins server.
2. Configure Jenkins to have access to the necessary plugins, such as the "File Operations Plugin" and any SCM-related plugins.
3. Create a new Jenkins pipeline job.

## Jenkins Pipeline

The Jenkins pipeline is responsible for automating the membership renewal process. It consists of the following steps:

1. SCM Integration: The pipeline fetches the latest code from a Bitbucket, which Jenkins configuration and the script.
2. File Uploader: The pipeline allows uploading a CSV file containing the membership ids.
3. Python Script Execution: The pipeline runs a Python script that reads the uploaded CSV file, and performs the renewal process.

## Usage

1. Configure the Jenkins pipeline job with the necessary parameters, such as Bitbucket repository URL and Jenkins file path.
2. Run the Jenkins pipeline job manually or schedule it to run at specific intervals.
3. Monitor the pipeline execution logs to track the progress and identify any issues.

## Contribution

Contributions to this repository are welcome! If you find any issues or have suggestions for improvement, please submit a pull request or open an issue.