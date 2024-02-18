# simpleapi
A simple API built for testing out Github CI/CD and deployment practices.

Goals of this repository:

I want to understand how to build a CI/CD pipeline in Github Actions.  
If I understand its full capabilities, it will help me make informed 
decisions on what else I need in my tech stack to make the workflow for a project
feel like a professional one.  


I want to understand the CD part of CI/CD by buidling and deploying docker images of the API to Google's Artifact Registry.

Follow this tutorial:
https://www.youtube.com/watch?v=6dLHcnlPi_U

Pretty much copy best practices from [this repo](https://github.com/sanders41/meilisearch-fastapi/tree/main)

### CI/CD activities

#### Code Quality & behavior
- code style
    - ruff
- testing behavior
    - pytest
- ensuring compliance with linting
    - precommit

#### Package management
- poetry

Here is a checklist of things I need to do:  
- [ ] use poetry for package management
- [ ] Set up precommit to enforce styling before committing to git
- [ ] Set up pytest for both:
    - [ ] the python project
    - [ ] the meilisearch
- [ ] explore [release drafter](https://github.com/marketplace/actions/release-drafter) github actions
