# GitHub Refresh Repository Invitation Tool
The primary tool in this repository is the refresh_invitations.py script.  There has recently been an issue with GitHub classroom where students are unable to access their private assignment repositories after they accept an assignment.  The private repository is created successfully and when I open the repository settings and click on the Collaborators page it shows the student's GitHub username with a status stating that the invite is pending. However, when they click the invite link in their email it shows that the invite has expired.  

To manually work around this issue, perform the following steps:  
1. Record the student's GitHub username.
2. Delete the student's account from the repository access list.
3. Add the student's GitHub account back to the repository access list with write permissions.
4. The student will now be listed with an invite pending status, similar to before

This generates an invite email from GitHub that is sent to the student's registered email address(es). You can also copy the invite link and email it directly to the student. Once the student clicks the updated invite link, they are able to access their repository without issue. (usually)


The refresh_invitation script automates this process as follows:

```
for each student_repo in github_organization:
    if student_repo created within the past 24 hours:
        for each account on student_repo.collaborators_list:
            if account.status is 'pending':
                remove_from_collaborators_list(account)
                add_to_collaborators_list(account,'write_access')

```

This script takes several minutes to run on organizations with 10s of 1000s of repositories. When the students are added to the repos, invite emails are sent to the student with the invite link. This is handled automatically by GitHub. Students just need to open this email and click the link to accept the invite.

## Usage
By default, the tool is set for "dry_run" mode which allows testing of the core functionality and configuration without affecting the student repositories.  When you are ready to run the code in a live environment, edit the refresh_invitations.py script and change the DRY_RUN variable from True to False.

```
...
DRY_RUN = False
...
```

You can run the script from the command-line as follows:
```
./refresh_invitations.py
```

## Tool Setup
First, clone the tool repo from GitHub
```
git clone git@github.com:lhindman/github-tools.git
```

### Python Packages
This tool has been tested with Python version 3.12.7. The only package I needed to install that was not part of the default python development environment was **python-decouple**.

### GitHub Access
1. Open Github Account Settings then select ***Developer Tools***  located at the bottom of the left panel.
2. Select ***Personal Access Token*** and then ***Token (classic)***  
3. Create a new Token with the following scopes: repo, admin:org
4. Set the name and expiration date as desired. I used an expiration date of 1 year
5. Record the new Personal Access Token

### Create Environment Configuration File
In the root of the github-tools repo create a .env file with the following variables set
```
GITHUB_TOKEN="<paste GitHub personal access token here>"
ORG="GitHub Classroom Organization"
```
