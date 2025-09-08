# GitHub Tools
The primary tool in this repository is the refresh_invitations.py script.  There has recently been an issue with GitHub classroom where students are unable to access their private assignment repositories after they accept an assignment.  The private repository is created successfully and when I own the repository settings and click on the Collaborators page it shows the student's GitHub username with a status stating that the invite is pending. However, when they click the invite link in their email it shows that the invite has expired.  To manually work around this issue, perform the following steps:  

1. Record the student's GitHub username.
2. Delete the student's account from the repository access list.
3. Add the student's GitHub account back to the repository access list with write permissions.
4. The student will now be listed with an invite pending status, similar to before

This generates an invite email from GitHub that is sent to the student's registered email address(es). You can also copy the invite link and email it directly to the student. Once the student clicks the updated invite link, they are able to access their repository without issue. (usually)


The refresh_invitation script automates this script as follows:

```
for each student_repo in github_organization:
    if student_repo created within the past 24 hours:
        for each account on repo collaborators list:
            if account.status is 'pending':
                remove_from_collaborators_list(account)
                add_to_collaborators_list(account,'write_access')

```

This script takes several minutes to run on organizations with 10s of 1000s of repositories.

## Tool Setup
