from graphviz import Digraph

def create_mpc_block_diagram():
    dot = Digraph(comment='FlowMPC Architecture', format='png')
    dot.attr(rankdir='LR', splines='ortho', compound='true')
    
    # Global styles
    dot.attr('node', shape='box', style='filled', fillcolor='white', fontname='Helvetica')
    dot.attr('edge', fontname='Helvetica', fontsize='10')

    # --- INPUTS ---
    with dot.subgraph(name='cluster_inputs') as c:
        c.attr(label='System Inputs', style='dashed', color='grey')
        c.node('Env', 'Environment (SDF)\nE', shape='parallelogram', fillcolor='#e1f5fe')
        c.node('State', 'Start (x0), Goal (xG)\nCost Params (ρ)', shape='parallelogram', fillcolor='#e1f5fe')

    # --- ENVIRONMENT ENCODING & PROJECTION (Algorithm 3) ---
    with dot.subgraph(name='cluster_embedding') as c:
        c.attr(label='Environment Representation & Projection\n(Algorithm 3)', color='purple', style='rounded')
        
        # VAE Encoder
        c.node('Encoder', 'VAE Encoder\nq_θ(h|E)', shape='component', fillcolor='#fff9c4')
        
        # Latent h
        c.node('h', 'Latent Embedding\nh', shape='ellipse', fillcolor='#fff9c4')
        
        # Projection Logic
        c.node('Prior', 'VAE Prior Flow\np_φ(h)\n(OOD Score)', shape='component', fillcolor='#ffe0b2')
        c.node('Projector', 'Gradient Descent\nmin(L_OOD + L_flow)', shape='diamond', fillcolor='#ffccbc')
        c.node('h_hat', 'Projected Embedding\nĥ', shape='ellipse', style='filled, bold', fillcolor='#ffab91')
        
        # Edges internal to embedding
        c.edge('Encoder', 'h')
        c.edge('h', 'Prior', label='Likelihood Check')
        c.edge('h', 'Projector', label='Initial h')
        c.edge('Prior', 'Projector', label='∇ L_OOD')
        c.edge('Projector', 'h_hat', label='Updated h')

    # --- CONTEXT GENERATION ---
    with dot.subgraph(name='cluster_context') as c:
        c.attr(label='Context Generation', style='invis')
        c.node('ContextNet', 'Context Network\ng_ω', shape='component', fillcolor='#dcedc8')
        c.node('Context', 'Context Vector\nC', shape='ellipse', fillcolor='#dcedc8')

    # --- FLOW GENERATION ---
    with dot.subgraph(name='cluster_flow') as c:
        c.attr(label='Generative Sampling', style='invis')
        c.node('Noise', 'Gaussian Noise\nZ ~ N(0, I)', shape='parallelogram', fillcolor='#f3e5f5')
        c.node('Flow', 'Conditional Flow\nf_ζ(Z, C)', shape='component', fillcolor='#e1bee7')
        c.node('FlowSamples', 'Flow Control Samples\nU_flow', shape='folder', fillcolor='#e1bee7')

    # --- MPC CONTROL (Algorithm 1 & 2) ---
    with dot.subgraph(name='cluster_mpc') as c:
        c.attr(label='MPC Controller\n(Algorithm 1: FlowMPPI / Algorithm 2: FlowiCEM)', color='blue', style='rounded')
        
        c.node('Nominal', 'Previous Nominal U\nor Mean μ', shape='box')
        c.node('Perturb', 'Gaussian/Colored\nNoise Sampling', shape='box')
        c.node('Dynamics', 'Dynamics Model\np(x\'|x, u)', shape='box')
        c.node('Cost', 'Cost Function\nJ(τ)', shape='box')
        c.node('Update', 'Update Logic\n(MPPI Weighted Sum \nor CEM Elite Fit)', shape='box', style='filled, bold', fillcolor='#b3e5fc')

        # Internal MPC edges
        c.edge('Nominal', 'Perturb', label='Shift')
        c.edge('Perturb', 'Dynamics', label='U_pert')
        c.edge('Dynamics', 'Cost', label='Trajectories τ')
        c.edge('Cost', 'Update', label='Costs S')

    # --- FINAL OUTPUT ---
    dot.node('Output', 'Optimal Control\nSequence U*', shape='doubleoctagon', fillcolor='#c8e6c9')

    # --- MAIN CONNECTING EDGES ---
    
    # 1. Input to Encoding
    dot.edge('Env', 'Encoder')
    
    # 2. Input to Context Net
    dot.edge('State', 'ContextNet')
    dot.edge('h_hat', 'ContextNet', label='Environment Feature')
    
    # 3. Context to Flow
    dot.edge('ContextNet', 'Context')
    dot.edge('Context', 'Flow', label='Conditioning')
    
    # 4. Flow Sampling
    dot.edge('Noise', 'Flow')
    dot.edge('Flow', 'FlowSamples')
    
    # 5. Connecting Flow Samples to MPC
    dot.edge('FlowSamples', 'Dynamics', label='U_flow (Samples/Elites)', color='blue')
    
    # 6. Connecting Flow Samples Back to Projection (The L_flow gradient)
    dot.edge('FlowSamples', 'Projector', label='∇ L_flow', style='dotted', constraint='false', color='red')

    # 7. Final Output
    dot.edge('Update', 'Output')
    dot.edge('Update', 'Nominal', label='Next Step', style='dashed')

    # Render
    dot.render('flow_mpc_diagram', view=False, cleanup=True)
    print("Block diagram generated as 'flow_mpc_diagram.png'")

if __name__ == "__main__":
    create_mpc_block_diagram()

# import matplotlib.pyplot as plt
# import matplotlib.patches as patches

# def create_mpc_block_diagram_plt():
#     # Create figure and axis
#     fig, ax = plt.subplots(figsize=(16, 10))
#     ax.set_xlim(0, 18)
#     ax.set_ylim(0, 10)
#     ax.axis('off')

#     # Helper function to draw blocks
#     def draw_box(x, y, w, h, text, color, shape='rect', bold=False):
#         if shape == 'ellipse':
#             patch = patches.Ellipse((x + w/2, y + h/2), w, h, linewidth=1.5, 
#                                     edgecolor='black', facecolor=color, zorder=3)
#         elif shape == 'diamond':
#             pts = [[x, y + h/2], [x + w/2, y + h], [x + w, y + h/2], [x + w/2, y]]
#             patch = patches.Polygon(pts, linewidth=1.5, edgecolor='black', facecolor=color, zorder=3)
#         elif shape == 'parallelogram':
#             patch = patches.Polygon([[x, y], [x + w*0.8, y], [x + w, y + h], [x + w*0.2, y + h]], 
#                                     linewidth=1.5, edgecolor='black', facecolor=color, zorder=3)
#         else: # rectangle
#             patch = patches.Rectangle((x, y), w, h, linewidth=1.5, 
#                                       edgecolor='black', facecolor=color, zorder=3)
#         ax.add_patch(patch)
#         ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
#                 fontsize=9, fontweight='bold' if bold else 'normal', zorder=4)

#     # --- CLUSTER: INPUTS ---
#     draw_box(0.5, 8, 2.5, 1, "Environment (SDF)\nE", '#e1f5fe', 'parallelogram')
#     draw_box(0.5, 6.5, 2.5, 1, "Start (x0), Goal (xG)\nCost Params (ρ)", '#e1f5fe', 'parallelogram')

#     # --- CLUSTER: ENVIRONMENT REPRESENTATION & PROJECTION (Algorithm 3) ---
#     # Background Grouping
#     group_3 = patches.Rectangle((3.5, 5.5), 6, 4, linewidth=1, edgecolor='purple', 
#                                 facecolor='none', linestyle='--', zorder=1)
#     ax.add_patch(group_3)
#     ax.text(6.5, 9.6, "Environment Representation & Projection\n(Algorithm 3)", 
#             color='purple', ha='center', fontweight='bold')

#     draw_box(4, 8, 2, 0.8, "VAE Encoder\nq_θ(h|E)", '#fff9c4') # Encoder
#     draw_box(4, 6, 2, 0.8, "Latent Embedding\nh", '#fff9c4', 'ellipse') # h
#     draw_box(7, 8, 2, 0.8, "VAE Prior Flow\np_φ(h)\n(OOD Score)", '#ffe0b2') # Prior
#     draw_box(7, 6.5, 2, 1, "Gradient Descent\nmin(L_OOD + L_flow)", '#ffccbc', 'diamond') # Projector
#     draw_box(7, 5.6, 2, 0.6, "Projected Embedding\nĥ", '#ffab91', 'ellipse', bold=True) # h_hat

#     # --- CLUSTER: CONTEXT & FLOW ---
#     draw_box(10.5, 7.5, 2, 0.8, "Context Network\ng_ω", '#dcedc8') # ContextNet
#     draw_box(13, 7.5, 1.5, 0.8, "Context Vector\nC", '#dcedc8', 'ellipse') # Context
#     draw_box(13, 9, 1.5, 0.6, "Gaussian Noise\nZ ~ N(0, I)", '#f3e5f5', 'parallelogram') # Noise
#     draw_box(15, 7.5, 2, 0.8, "Conditional Flow\nf_ζ(Z, C)", '#e1bee7') # Flow
#     draw_box(15, 6, 2, 0.8, "Flow Samples\nU_flow", '#e1bee7') # FlowSamples

#     # --- CLUSTER: MPC CONTROLLER (Algorithm 1 & 2) ---
#     group_mpc = patches.Rectangle((10.5, 0.5), 6.5, 5, linewidth=1, edgecolor='blue', 
#                                   facecolor='none', linestyle='--', zorder=1)
#     ax.add_patch(group_mpc)
#     ax.text(13.75, 5.2, "MPC Controller (Algo 1: FlowMPPI / Algo 2: FlowiCEM)", 
#             color='blue', ha='center', fontweight='bold')

#     draw_box(11, 4, 2, 0.8, "Previous Nominal U\nor Mean μ", '#ffffff') # Nominal
#     draw_box(14, 4, 2, 0.8, "Gaussian/Colored\nNoise Sampling", '#ffffff') # Perturb
#     draw_box(14, 2.5, 2, 0.8, "Dynamics Model\np(x'|x, u)", '#ffffff') # Dynamics
#     draw_box(14, 1, 2, 0.8, "Cost Function\nJ(τ)", '#ffffff') # Cost
#     draw_box(11, 1, 2, 0.8, "Update Logic\n(Weighted Sum/Elite)", '#b3e5fc', bold=True) # Update

#     # --- FINAL OUTPUT ---
#     draw_box(8, 1, 2, 0.8, "Optimal Control\nSequence U*", '#c8e6c9', 'ellipse', bold=True)

#     # --- DRAWING EDGES ---
#     arrow_props = dict(arrowstyle='->', lw=1.2, color='black')
    
#     # Inputs to Algo 3 & Context
#     ax.annotate('', xy=(4, 8.4), xytext=(2.5, 8.4), arrowprops=arrow_props) # Env to Encoder
#     ax.annotate('', xy=(10.5, 7.8), xytext=(3, 7), arrowprops=arrow_props) # State to ContextNet
#     ax.annotate('', xy=(10.5, 7.6), xytext=(9, 5.9), arrowprops=arrow_props) # h_hat to ContextNet

#     # Inside Algo 3
#     ax.annotate('', xy=(5, 6.8), xytext=(5, 8), arrowprops=arrow_props) # Encoder to h
#     ax.annotate('', xy=(7, 8.2), xytext=(6, 6.4), arrowprops=arrow_props) # h to Prior
#     ax.annotate('', xy=(8, 7.5), xytext=(8, 8), arrowprops=arrow_props) # Prior to Projector
#     ax.annotate('', xy=(8, 6.2), xytext=(8, 6.5), arrowprops=arrow_props) # Projector to h_hat

#     # Flow generation
#     ax.annotate('', xy=(13, 7.9), xytext=(12.5, 7.9), arrowprops=arrow_props) # ContextNet to C
#     ax.annotate('', xy=(15, 7.9), xytext=(14.5, 7.9), arrowprops=arrow_props) # C to Flow
#     ax.annotate('', xy=(15.5, 8.3), xytext=(14.5, 9.1), arrowprops=arrow_props) # Noise to Flow
#     ax.annotate('', xy=(16, 6.8), xytext=(16, 7.5), arrowprops=arrow_props) # Flow to FlowSamples

#     # MPC Internal
#     ax.annotate('', xy=(14, 4.4), xytext=(13, 4.4), arrowprops=arrow_props) # Nominal to Perturb
#     ax.annotate('', xy=(15, 3.3), xytext=(15, 4), arrowprops=arrow_props) # Perturb to Dynamics
#     ax.annotate('', xy=(15, 1.8), xytext=(15, 2.5), arrowprops=arrow_props) # Dynamics to Cost
#     ax.annotate('', xy=(13, 1.4), xytext=(14, 1.4), arrowprops=arrow_props) # Cost to Update
#     ax.annotate('', xy=(11, 3.9), xytext=(11.5, 1.8), arrowprops=arrow_props) # Update to Nominal (feedback)

#     # External to MPC
#     ax.annotate('', xy=(16, 3.3), xytext=(16, 6), arrowprops=dict(arrowstyle='->', lw=1.2, color='blue')) # FlowSamples to Dynamics
#     ax.annotate('', xy=(8, 1.4), xytext=(11, 1.4), arrowprops=arrow_props) # Update to Output
    
#     # L_flow gradient feedback (Dotted Red)
#     ax.annotate('∇ L_flow', xy=(9, 6.8), xytext=(15, 6.4), 
#                 arrowprops=dict(arrowstyle='->', lw=1, color='red', linestyle=':'))

#     plt.tight_layout()
#     plt.savefig('flow_mpc_matplotlib.png', dpi=300)
#     plt.show()

# if __name__ == "__main__":
#     create_mpc_block_diagram_plt()