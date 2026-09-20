# Publishing this project on GitHub

Suggested repository name: **ev-rebound-maharashtra**

Suggested description: **Electric two-wheelers, rooftop solar and travel rebound in Maharashtra: public explainer, academic working paper and reproducible scenarios.**

Suggested topics: `electric-vehicles`, `energy-economics`, `rebound-effect`, `rooftop-solar`, `maharashtra`, `transport`, `research`.

## Browser route

1. Extract the project ZIP on your computer.
2. In your GitHub account, create a new repository named `ev-rebound-maharashtra`. Choose Public if the aim is public dissemination. Use the description above. The package already has a README; a generated README is unnecessary.
3. Use the repository's file-upload option to upload the **contents** of the extracted project folder, preserving its subfolders. Place `README.md` at the repository root. Uploading only the ZIP will not display the paper and figures as a browsable project.
4. Commit with the message `Add public explainer and academic working paper v1.0.0`.
5. Open the README, both Markdown editions and both PDFs on GitHub to confirm their links and rendering.
6. Add the actual repository URL to `CITATION.cff` and the README citation. Create a `v1.0.0` release after the byline and content reflect the author's intended public version. A release does not automatically create a DOI.

The files are small enough for an ordinary research repository. Choose any reuse licence deliberately; the package does not preselect one.

## Authenticated command-line route

If Git and GitHub CLI are available and authenticated, run these commands from the extracted project directory. This creates a new public repository under the authenticated account; use the browser route for an existing repository or a different destination.

```bash
git init -b main
git add .
git commit -m "Add public explainer and academic working paper v1.0.0"
gh repo create ev-rebound-maharashtra --public --source=. --remote=origin --push
```

Use your own configured Git author identity. Do not paste access tokens into project files. If the repository name already exists, inspect it before choosing whether to update it or use another name.

## Presenting it in a research portfolio

Describe the current work as an independent, AI-assisted conceptual working paper with reproducible scenario analysis. Its strengths are transparent assumptions, explicit limitations and a proposed route to evidence. A future version can add a pilot dataset or a field study once that work has actually been completed.

## Official GitHub guidance

- [Quickstart for repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories)
- [About citation files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files)

Publishing steps were checked against GitHub's documentation on 20 September 2026. The interface may change.
