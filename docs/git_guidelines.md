# Git guidelines to interact with this library

This library will follow GitFlow Workflow to make updates, work on branches, pull requests and so on. [Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

## Overview of the use of branches

Branches Structure

- main: Production-ready releases for deployment on mainnet. This branch will work based on tags, which is going to be the history out of all the releases starting from 0.1.x. The frequency of merge might be quite often, but less frequent than “dev”.
- develop: Will target the testing side and would have the means for deployments on testnets, will also aggregate any feature ready for launch before being merged to “main”. This branch is expecting continuous merges and pull requests.
- feature_< name >: Temporal branches based on current features being developed, there can be as many as needed. It might be merged with develop only if the user story is fully satisfied, this makes it possible to retake a branch name if a new requirement explicitly calls for this module/feature.
- hotfix_name: As “feature” branches, these will be temporal branches, but are expected to be immediately merged to dev once the bug is considered to be resolved, if necessary one new branch can be reactivated, and its purposes are to allow for continuous development and deployment. NOTE: Features can also have their own bug branches while in development phases.
- release/major_version: Off-branching from “main”, once a milestone is achieved there might be a need to refresh main while keeping a separate history of past releases histories.

## Ways to collaborate

> We welcome all sort of contributions. 

If you want to contribute, please bear in mind the following:

Create a new branch from develop branch. Feature branches always reference the develop branch so develop branch is the main point of reference and the destination branch where the merge action will be applied. 

    git checkout develop
    git checkout -b feature_[your_branch_name]

Continue your work and use git as normally. All your changes wil get tracked under your own branch.

When you are done open a pull request and make sure to target the develop branch. 


