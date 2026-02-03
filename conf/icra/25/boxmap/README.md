### BoxMap: Efficient Structural Mapping and Navigation
This document summarizes the core contributions and methodology of the paper "BoxMap: Efficient Structural Mapping and Navigation", focusing on its' main ideas and the core blocks.
- [Original Paper](https://github.com/nicewang/robotics_papers/tree/assets/conf/icra/25/boxmap/original_paper)
- Summarization Download: TBD

#### Summarized Block-Diagram
![Block-Diagram](fig/clea_experimental_workflow_diagram.png) 

#### Orig Paper Citation
```BibTex
@inproceedings{mohammad2024gp,
@inproceedings{wang2025boxmap,
  title={Boxmap: Efficient structural mapping and navigation},
  author={Wang, Zili and Allum, Christopher and Andersson, Sean B and Tron, Roberto},
  booktitle={2025 IEEE International Conference on Robotics and Automation (ICRA)},
  pages={6401--6407},
  year={2025},
  organization={IEEE}
}
```

##### draft
| Component | Input | Primary Function | Core Logic and Value |
| :--- | :--- | :--- | :--- |
| CNN Backbone | Raw TSDF / Images | Dimensionality Reduction and Local Feature Extraction | (1) **Downsamples** inputs into high-level semantic feature maps.  <br>(2) Reduces pixel count to prevent O(N^2) complexity explosion in Attention. <br>(3) Provides **Inductive Bias** (Translation Invariance).</br> |
| Transformer Encoder | Feature Maps | Global Context Encoding | Uses **Self-attention** to model long-range dependencies between pixels (e.g., relating distant walls). |
| Object Queries | Learnable Vectors | Entity Proposals | Acts as M placeholders (occupants) to query potential objects in the scene. |
| Transformer Decoder | Queries + Encoded Features | Object Manifestation | Maps queries to specific **Box Embeddings** via **Cross-attention**. |
| Decoder Self-Attention | Intermediate Queries | Parallel Coordination | Unmasked Attention allows queries to communicate and avoid redundant detections (Parallel de-duplication). |
| Hierarchical Loss | Predicted Boxes vs. GT | Detail Enhancement | Subtracts large objects (rooms) from TSDF to focus on small topological details (doors). |
| Prediction Heads | Box Embeddings | Geometric Mapping | Projects embeddings into 3D box coordinates and class labels. |
```txt
low-level measurements can then be leveraged to achieve
high-level goals 

(1) What is the problem?
- Navigation in Complex and Unknown (a.k.a Unmapped or Partial Sensed) Environments
- Robot Navigation in Resource-Constrained Scenarios
- Topological Graph Generation and Real-Time Updating -> Topological Graph Prediction (what actually do)


(2) Why need to solve this problem?
- Traditional standard navigation methods require maintenance of detailed environment representations.
- Maintaining detailed environment representations is resource-expensive.
- Demands for running within resource-constrained scenarios.


(3) How is it different from prev.?


- Compared with traditional pixel-wise semantic segmentation, wall entities identification \& clustering: 
	- Utilizing deep learning to learn from prior experience.


Anchor-free
- Compared with Anchors based Bounding Boxes Prediction + CNN-RNN (or CNN-GCN) base Corners Detection:
	- Transformer encoder-decoder architecture to eliminate anchor generation;
	- Truncated Signed Distance Function (TSDF) based global loss to eliminate Non-Maximum Suppression (NMS);
	- In Summarization, an end-to-end DEtection TRansformer (DETR) method to reduce reliance on hand-crafted components (NMS, anchor generation, etc). 
 


- Compared with other DETR + regression/classification:
	- Box embeddings/representations: Using bounding boxes as primitives of environment (core point).


(4) Why is it better than prev.? (Advantages)
- BoxMap (bounding boxes as interpretable embeddings, within uses a DETR-like framework) leading to no need for multi-resolution representations and extra post-processing.
- Lower Computational Costs -> Low-Resource
- Less Space Complexity of Map/Graph (BoxMap representation scales quadratically with the number of rooms)
- Better Small Details Detection by Utilizing Hierarchical Loss
- Enabling downstream decision making tasks (planning & navigation, etc) to generate shorter trajectories.

(5) What is the approach itself?
- Top-down, Low-Resource Robotic Navigation in Unmapped (or Partial Sensed) Environments
end-to-end BoxMap, a Detection-Transformerbased architecture
- transfers From low-level measurements (points, lines) to topological maps (i.e., high-level semantic representations (entities+relations))
- A DEtection TRansformer (DETR) based end-to-end method

(6) What are the applications of it?
- Downstream: "Lyapunov Neural Network with Region of Attraction Search"?

- a robot equipped with a 2-D laser scanner tasked with
exploring a residential building

Open Questions: "Sim-to-Real"?
```
