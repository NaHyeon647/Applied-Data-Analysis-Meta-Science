# ADAMS assignment 1 a questionable practice

In meta-science, we often talk about scientific fields and problems across many publications. In a course, we can’t even do a single full study. But what we can do, is simulate doing many studies in a row, where we control “the truth”. If our simulation is any good, we can use that to see the expected results of studies where a true effect exists, where actually nothing is going on, or where the researchers make some questionable choices. This is how we will do it:

1. Come up with a study plan
2. Make hypothetical data for the study
3. Analyse the made-up data with an appropriate technique
4. Simulate what would happen if you were to repeat your study
5. Commit a questionable research practice inside the simulation
6. Report on the results of your simulations and explain what we see

We will do this in steps, with weekly deadlines and time for feedback and questions.

## Practicalities

You will only be graded for the final, full report. The intermediate milestones have to be handed in (pass/fail), but they don’t have to be perfect. Use them to ask questions and get feedback on your work. If you run into any issues, please let the teachers know.

## 1 Part A: Research proposal

### Description

The first task is to make assignment groups, and come up with an imaginary study. For the purposes of this assignment, it doesn’t matter much what the focus of your research is, so you might as well pick something you find interesting. If you’re really stuck, the Appendix has some examples to get you started. Things to keep in mind when you pick something:

- Is it an explanatory question, so something with a causal reasoning?
- Doyou have a hypothesis?
- Would it be possible to answer the question, in an experiment or in an observational study with statistical control?
- What are the variables you would need to measure, to answer the question?
- Is it feasible to answer the question with a relatively simple statistical test?

You are not going to actually conduct the study, but you will randomly generate (simulate) data and analyse those, in the coming weeks.

To help you with the statistical choice, you can have a look at this website: https\://sheffield.ac.uk/mash/stats-resources/choosing

We will have a closer look at the statistics next week, but pick an appropriate test from this page. Try to stick to methods you are familiar with (so probably not repeated measures ANOVA or mixed models), and adjust the experimental design if none of those works.

### Hand in

1. A pdf document with a title, student names and numbers, date and:

   - Ashort context of the research (why it is interesting)
   - The research question
   - Your hypothesis about the research question (what you think is true)
   - The null hypothesis (what would you expect to find if there’s no relationship / effect)
   - Ashort description of the study design (how you would conduct the study)
   - Adescription of the variables you measure (including measurement level, possible values, units) and the sample size (and group sizes if applicable)
   - Afirst proposal for the analysis pipeline (which statistical test, on which variables)

Write this down in essay format, of max. 500 words.

If you have any questions for the teacher, you can add those at the end.

## 2 Part B: Synthetic data

### Description

We are now going to manufacture data for our study. In later weeks we will write loops to repeat this process multiple times, but this week we focus on a single synthetic dataset and what it looks like.

Write code, in R or Python, to randomly generate the observations in your dataset. This means drawing numbers from distributions (for example with rnorm() in R or rng.normal() in Python) and making sure that you can build in the effect of interest of your study. This effect should be a parameter that you can tweak, for example as the difference in means between two groups or the strength of the relationship between two numerical variables. If you have any covariates in your model, you can simulate them as independent or correlated.

Visualise the data in one or more suitable plots. Are the values of your variables realistic? Play around with the effect size parameters to see what this does to your data and plots

Make one version of the dataset with a realistic effect of interest, and one where no true effect exists (so the null hypothesis is true). The difference between these two may be small...

### Hand in

1. A pdf document containing:

   - The research proposal of part A, updated where necessary
   - Adescription of how you simulated the data, detailing:
     - The main parameters, like sample size and effect size
     - The distributions used to draw values
     - Any manipulations you performed on the values to make them more realistic (rounding, truncating)
   - Visualisations of both of the simulated datasets (one with and one without an effect)
   - Ashort description of what we see in the visualisations and how that links to your research question

From here on there’s no explicit word limit. Just try to make it concise and complete, ask the teacher when you’re unsure.

2. Your script (.R or .py), with comments to explain every part of the simulation. Make sure to specify a seed in your code, for reproducibility purposes.

## 3 Part C: Simulated analysis

### Description

Last week you made two datasets, one in line with having an actual effect (alternative hypothesis) and one where no true effect exists (null hypothesis). Now it is time to actually analyse the data. But first, is the statistical model you had in mind suitable for this data? Check the assumptions of that model against the simulated data. You may need to pick a different model, or transform some of your variables. But be careful: are you exploring and explaining using the same data? What could go wrong here?

Now fit your statistical model of choice and report the relevant p-value(s) and effect(s). Do you find the (absence of) effects that you expect? Are your results exactly in line with the parameters you set? Should they be? What does the difference you find depend on?

The next step is to repeat the whole process (generate the data, run the test, record the outcome) many times over. A single study gives you one result, but it is only one of the possible outcomes. Simulating many studies shows you the whole distribution: what you would see if thousands of researchers ran the same study, each with their own data sample.

In your code, write a loop to sample data, do the test, and store the relevant results. Do this twice, one simulation loop under the alternative hypothesis (a reality where an effect exists), and one under the null (where “nothing is going on”).

Based on your results, you can now estimate:

- the type I error rate;
- the type II error rate and the statistical power (for the parameters in your simulation);
- how much the estimated effect varies from study to study.

In your simulation loops, you may want to set the number of repetitions (“studies”) to be some low number at first (for time-saving) and then increase it when generating the final results. The best number to pick depends on the speed of your code/computer and the precision you want in the estimates.

### Hand in

1. A pdf document containing:

   - Parts A and B, updated where necessary
   - Ashort description of the assumption checks you performed, with relevant plots and interpretation, and changes to your model or data (if any)
   - The results of the analyses on the two simulated datasets and answers to the questions asked above
   - Areport of the simulation study:
     - Visualise your results, make plots of the distributions of the relevant outcomes
     - Report your estimates of type I error rate, type II error rate, power, and estimated effects
     - Interpret what you find, and what those findings depend on

Hint for the final sub-point: what would you expect if the researchers had, for example, a larger sample size?

2. Your script (.R or .py), with comments to explain every part of the simulation.

## 4 Part D: Simulation with QRP

### Description

It’s finally time to commit some questionable practices! In the previous parts of this assignment we have seen what we can expect from a study that is conducted in a proper way. But researchers don’t always do things the proper way. Look at the questionable research practices discussed in the lecture. Pick one or two of those that fit your study.

Perform a new simulation study, under alternative and null, where you implement the QRP(s). You may need some conditional statements in your code to get this working, so it is a bit of a puzzle. Remember that QRPs involve practices that can be valid data-analytic choices, but become problematic because they are applied in a selective way.

Compare your new results to those of last week. What happens to the type I error rate, type II error rate, power and estimated effects? Why are these changes problematic, what would be their consequences in the real world?

In the second half of this course, we will discuss ways to deal with these problems. Perhaps you can already think of some solutions?

### Hand in

1. A first version of the full report (in pdf), containing:

   - Parts A-C, updated where necessary
   - Adescription of the QRP(s) you have implemented: how they work in the real world (actions of the researchers) and how this is represented in your code
   - Visualisations and an interpretation of the results: what are the effects of committing the QRP(s) on the numbers you calculate in the simulations
   - Ashort discussion of the implications for real research
   - Asection containing your AI statement: which LLMs you used, for what, and how this shaped the report

2. Your script (.R or .py), with comments to explain every part of the simulation.

## 5 Full report

### Description

For the final deadline, update your report using the feedback you have received.

Read everything once again from the top to make sure it all follows logically. Some final checks:

- Does each team member support all the statements made in the report and understand all lines of code?
- Nowyou have learned a bit more about visualisation, have another look at your plots and improve them
- Does your script run, from start to finish, in a clean session, and match the reported results exactly?
- Are all the parts included (A-D), with the AI statement as well?

You will have a short oral exam about the assignment (more info on Brightspace). Together with the report you hand in, this is the basis for your assignment 1 grade.

### Hand in

1. The full report (pdf)

2. The full script (.R or .py)

## 6 Appendix: examples of research questions

These are some research questions, created using Claude (Opus 5), to show the kinds of questions you could ask. Don’t pick from the list, but use it for inspiration.
- Does the time of day a notification is sent change how quickly people open it?
- Dosongs with faster tempos get skipped less often?
- Dopeople trust a chatbot’s answer more when it shows a confidence score?
- Does paying data annotators per hour instead of per item change the quality of their labels?
- Does replacing a lawn with wildflowers bring more pollinators?
- Does adding a “why you’re seeing this” explanation to a recommendation make people more likely to click it?
- Does a supermarket sell more fruit when it’s placed near the entrance?
- Doprogrammers finish a task faster with an AI coding assistant than without one?
- Does a warning label on a deepfake video change how much people believe it?
- Docyclists ride faster on days with better air quality, once you account for temperature and wind?
- Dodelivery riders take more risks when the app shows a countdown timer?
- Does a hospital’s waiting time depend on how many staff are on shift, after accounting for how busy the day is?
- Dobigger programming teams close bug reports faster, after taking bug severity into account?
- Dostudents write better code when they explain it out loud first?
- Does a short training session help people spot AI-generated text?
- Does a data centre’s energy use depend on outdoor temperature, once you account for how much work it is doing?
- Dosolar panels produce less power as they get older, once you separate that from dust and shading?
- Dowolves in a national park move further on nights with a full moon?
- Does a job advert get more applications from women when it drops words like “competitive” and “dominant”?
- Does a longer product description keep people on the web page longer?
- Does labelling a photo as AI-generated change how realistic people say it looks? 7 &#x20;
