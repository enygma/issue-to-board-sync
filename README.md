# issue-to-board-sync
A workflow for updating a project board with issue contents when created

## Setup

Here's how to set this script up and customize it:

1. Update the `ORG` value in the workflow to your org name
2. Update the `PROJECT_ID` to the ID of your project
3. Create a repository secret called `MY_GH_TOKEN` that contains a PAT with access to both issues and projects. If you're using it our org, it will need SSO access too.

The format for the information in the issue body should be the type (like `'Impact Level', 'Effort Level', 'Confidence Level', 'Risk Level'`) followed by a colon and a space. The regex is pretty specific about that.

Also make sure to set up the project board workflow to auto-add issues to the board. Thankfully it seems that our system adds it to the board before this workflow has time to finish.