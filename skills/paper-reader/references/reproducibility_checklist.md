# Reproducibility Checklist

This checklist guides the Questioner agent in systematically assessing whether a paper can be reproduced. Questions are organized by paper type. Not all items apply to every paper — adapt based on the paper's nature.

## Universal (All Paper Types)

- [ ] Is the problem clearly and formally defined?
- [ ] Is the proposed method described at a level of detail sufficient for reimplementation?
- [ ] Are all design decisions justified (not just stated)?
- [ ] Are the assumptions underlying the method explicitly listed?
- [ ] Is the evaluation methodology clearly specified?
- [ ] Are the evaluation metrics clearly defined?
- [ ] Is there a comparison against reasonable baselines?
- [ ] Is the code or implementation available? If so, where?
- [ ] Are the datasets/benchmarks publicly available?
- [ ] Is the paper self-contained, or does it rely on external technical reports for key details?

## ML / Deep Learning Papers

### Model Architecture
- [ ] Is the exact architecture specified (layers, dimensions, activations)?
- [ ] Are weight initialization schemes specified?
- [ ] Is the number of parameters reported?
- [ ] Are any pretrained components specified with their source?

### Training
- [ ] Is the loss function fully defined (including any regularizers)?
- [ ] Is the optimizer specified with all hyperparameters (lr, beta1, beta2, epsilon, weight decay)?
- [ ] Is the learning rate schedule specified?
- [ ] Is the batch size specified?
- [ ] Is the number of training epochs/steps specified?
- [ ] Are early stopping criteria specified?
- [ ] Are data augmentation techniques fully described?
- [ ] Is the train/validation/test split specified?
- [ ] Are random seeds specified for reproducibility?

### Hardware / Software
- [ ] Is the GPU/TPU model and count specified?
- [ ] Is the training time/wall-clock time reported?
- [ ] Are library versions specified (PyTorch, TensorFlow, CUDA, etc.)?
- [ ] Is the OS specified?

### Evaluation
- [ ] Are error bars or standard deviations reported?
- [ ] Are statistical significance tests performed?
- [ ] Is the evaluation protocol clearly described (e.g., how predictions are aggregated)?
- [ ] For generative models: are decoding/sampling parameters specified?

## Systems Papers

### System Design
- [ ] Is the system architecture clearly described (components, data flow)?
- [ ] Are all system parameters and their default values listed?
- [ ] Are configuration files or deployment scripts available?
- [ ] Is the system's dependency on specific hardware/OS features documented?

### Performance Evaluation
- [ ] Is the benchmarking methodology clearly described?
- [ ] Are the benchmark specifications (queries, workloads) available or described?
- [ ] Is the hardware configuration fully specified (CPU model, cores, RAM, disk, network)?
- [ ] Is the software stack versioned (OS, compiler, libraries)?
- [ ] Is cold-start vs. warm-start behavior documented?
- [ ] Are performance metrics clearly defined (latency percentiles, throughput measurement window)?
- [ ] Is the system compared under fair conditions (same hardware, same workload)?
- [ ] Are failure modes or scalability limits discussed?

## Theory / Algorithm Papers

- [ ] Is every theorem stated with its full set of assumptions?
- [ ] Are proof sketches provided for all major results?
- [ ] Are the assumptions justified (why are they reasonable)?
- [ ] Is the tightness of bounds discussed?
- [ ] Are there counterexamples showing why assumptions are necessary?
- [ ] Is the algorithm presented in executable pseudocode?
- [ ] Is the complexity analysis complete (time + space, worst-case + average-case)?
- [ ] Are there empirical validations of the theoretical claims?

## Empirical / Data Analysis Papers

- [ ] Is the data collection methodology fully described?
- [ ] Are data cleaning and preprocessing steps documented?
- [ ] Are the characteristics of the dataset described (size, distribution, biases)?
- [ ] Is the data available for download? If not, why?
- [ ] Are confounding variables discussed?
- [ ] Is the statistical methodology appropriate and justified?
- [ ] Are effect sizes reported (not just p-values)?
- [ ] Are limitations of the data discussed?

## HCI / Design Papers

- [ ] Is the user study design fully described (participants, tasks, procedure)?
- [ ] Are participant demographics reported?
- [ ] Is the recruitment method described?
- [ ] Are the study materials available (questionnaires, task descriptions)?
- [ ] Is the analysis methodology (qualitative or quantitative) clearly described?
- [ ] Are ethical approvals mentioned?

## Critical Red Flags

These indicate serious reproducibility concerns regardless of paper type:

- [ ] Key hyperparameters are missing with no justification
- [ ] The method relies on proprietary/unavailable data
- [ ] The method relies on proprietary/unavailable code
- [ ] Results are reported without any measure of variance
- [ ] The paper cherry-picks baselines that are known to be weak
- [ ] The evaluation uses a different metric than what was optimized for
- [ ] Ablation studies are absent for a method with multiple components
- [ ] The paper claims SOTA but compares against outdated baselines
