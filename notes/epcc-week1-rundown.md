# Week 1 (EPCC, Cirrus) rundown, for the final presentation

From the team's "EPCC Cluster Challenge" slides (team Drive). Reconstructed 25 Oct 2026.

- Task: HPL and HPCG on 1 to 4 Cirrus nodes, balancing GFLOPS against GFLOPS/W (energy from `sacct`).
  Marks: HPL efficiency 25, HPCG efficiency 25, scaling 20, presentation 30.
- Node: 2 × AMD EPYC 9825, 288 cores, 768 GB, 8 NUMA regions of 36 cores, 24 CCDs of 12 cores.
- HPL best efficiency 12.79 GFLOPS/W on 1 node (N=250,000, NB=320, 32 ranks × 9 threads, Cray -O3 -flto),
  about 15,345 GFLOPS. N, NB and layout improved speed and efficiency together; 4 nodes were 2.15× faster
  but used 64% more energy; compiler flags barely mattered (time is in LibSci).
- HPCG: GNU about 29% faster than Cray; pure MPI (288 × 1) about 2× hybrid because the reference smoother
  doesn't thread. Best efficiency 0.1376 GFLOPS/W (144 ranks × 2 cores, 1 node); best speed 532 GFLOPS on
  4 nodes, 96–97% scaling efficiency, about 6% less efficient than 1 node.
- One node: HPL ~15,345 vs HPCG ~134.5 GFLOPS at similar power: compute-bound vs memory-bound.
- What we'd do differently: a day-0 recon job (sinfo, module avail, lscpu, numactl -H), choose layouts
  that match the hardware instead of sweeping blindly, one parameterised job script with job arrays and a
  CSV row per run from the start (what we did from week 2).
