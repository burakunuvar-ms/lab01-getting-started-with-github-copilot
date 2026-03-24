## Step 5: Using GitHub Copilot within a Pull Request

Congratulations! You are finished with coding for this exercise (and VS Code). Now it's time to merge our work. 🎉 To wrap up, let's learn about two limited-access Copilot features that can speed up our pull requests!

### 📖 Theory: GitHub Copilot for pull requests - OPTIONAL 

#### Copilot pull request summaries

Typically, you would review your notes and commit messages then summarize them for your pull request description. This may take some time, especially if commit messages are inconsistent or code is not documented well. Fortunately, Copilot can consider all changes in the pull request and provide the important highlights, with references too!

#### Copilot code review

More eyes on our work is always useful so let's ask Copilot to do a first pass before we do a normal peer review process. Copilot is great at catching common mistakes that are fixed by simple adjustments, but please remember to use it responsibly.

> [!NOTE]
> These features are only available on paid plans of **GitHub Copilot**.
> [[docs]](https://docs.github.com/en/copilot/get-started/plans)

### :keyboard: Activity: Summarize and review a PR with Copilot

Both **Copilot pull request summaries** and **Copilot code review** have limited access, so this activity is mostly optional. If you don't have access, skip the optional steps of this activity.

1. In a web browser, open another tab and navigate to your exercise repository.

1. You might notice a **notification banner** suggesting to create a new pull request. Click that or use the **Pull Requests** tab at the top. Please use the following details:

<img alt="Create pull request page" width="450px" src="https://github.com/{{full_repo_name}}/raw/main/src/static/images/pull-request.png">

   - **base:** `main`
   - **compare:** `accelerate-with-copilot`
   - **title:** `Improve student activity registration system`

1. In the PR description toolbar click the **Copilot** icon and **Summary** action. After a moment, Copilot will add a description based on your changes. 📝 Then click **create a new pull request**

   <img alt="Copilot summarize button" width="450px" src="https://github.com/{{full_repo_name}}/raw/main/src/static/images/copilot-summarize-button.png">

1. (Optional) In the right side information panel at the top, locate the **Reviewers** section and click the **Request** button next to a **Copilot icon**. Wait a moment for Copilot to add a review comment to your pull request!

   <img alt="Copilot review button" width="300px" src="https://github.com/{{full_repo_name}}/raw/main/src/static/images/copilot-review-button.png">

   > 💡 **Tip:** Notice a log entry that Copilot was requested for a review.

1. At the bottom, press the **Merge pull request** button. Nice work! You are all done! 🎉

1. Wait a moment for Mona to check your work, provide feedback, and post a final review of this exercise!
