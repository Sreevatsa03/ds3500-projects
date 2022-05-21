# DS3500 Projects

This repo contains small projects I completed in my DS3500 course (Advanced Programming with Data) at Northeastern University.

## [Exploration of Artists Demographics](artists_demographics_sankey)

I explore the demographics of artists represented at the Museum of Contemporary Art Chicago. This is done by visualizing the relationships between artists' nationality, birth decade, and gender.

- Read, filter, and store data from JSON files of artists' demographics
- Generate sankey diagrams between demographics (nationality to gender, nationality to birth decade, gender to birth decade)
- Write report on inclusion, diversity and bias in the 'art world'

## [Reusable Framework for Natural Language Processing](crispr_discussion_nlp)

This project revolves around creating a reusable NLP library used to analyze and compare texts. I fed my framework texts discussing the ethics behind the emerging CRISPR technology.

- Gathered textual data to analyze, including research papers and op-ed's
- Implemented framework to parse, clean (remove stop words and lemmetize), and gather summary statistics (word count, num unique words, heap's law) on JSON, PDF, and txt files
- Compared texts with sentiment analysis (polarity and subjectivity), heap's law analysis, and sankey diagrams by establishing framework to easily create and customize them

## [Production Planning using Evolutionary Computing](production_planning_evolutionary)

We explore intelligent decision support by leveraging functional programming to build a factory machine production scheduler.

- Imlemented an evolutionary computing framework with pickling to generate and visualize tradeoffs in production scheduling
- Created 3 fitness criteria and 3 agents to solve scheduling problems (setups, priority, delays)
- Visualize tradeoffs between fitness criteria through 3D scatter plot and pairplot

## [Multi-Species Ecological Simulation](ecological_simulation)

In this project, I create a basic ecological simulation of 2 competing species of rabbits with different reproduction and movement capabilities in a field of grass.

- Implemented Rabbit and Field objects with modifiable values, such as grass growth rate, field size, initial population size, etc.
- Animate changing field over time, and implement command line options of simulation speed and number of generations
- Visulize differnce in species' population with animated plot and 3d scatter plot of species' population vs grass popluation

