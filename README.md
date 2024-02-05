# simpleapi
A simple API built for testing out Github CI/CD and deployment practices.

Goals of this repository:

I want to understand how to build a CI/CD pipeline in Github Actions.  
If I understand its full capabilities, it will help me make informed 
decisions on what else I need in my tech stack to make the workflow for a project
feel like a professional one.  


I want to understand the CD part of CI/CD by deploying to Render. 
Render seems like the fastest solution to a working deployment. Then,
migrating to the google cloud seems like the best option because Render does
not seem that cheap, and doesn't provide autoscaling.


Instead of deploying to Render. I want github to manage creating and publishing Docker images to Google's Artifact Registry. From there, inside of google we can configure things to automatically start a compute engine with specified images.

Follow this tutorial:
https://www.youtube.com/watch?v=6dLHcnlPi_U



This was written as part of the next patch version 0.1.1

This was written as part of the next patch. version 0.1.2

This is written as new-feature 1.

This is written as new-feature 2.
