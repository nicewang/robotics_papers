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
        c.node('Env', 'Environment (SDF)\nE', shape='ellipse', fillcolor='#e1f5fe')
        c.node('State', 'Start (x0), Goal (xG)\nCost Params (ρ)', shape='ellipse', fillcolor='#e1f5fe')

    # --- ENVIRONMENT ENCODING & PROJECTION (Algorithm 3) ---
    with dot.subgraph(name='cluster_embedding') as c:
        c.attr(label='Projection\n(Algorithm 3)\n(OOD -> In-Distribution)', color='purple', style='rounded')
        
        # VAE Encoder
        c.node('Encoder', 'VAE Encoder\nq_θ(h|E)', shape='component', fillcolor='#fff9c4')
        
        # Latent h
        c.node('h', 'Latent h', shape='ellipse', fillcolor='#fff9c4')
        
        # Projection Logic
        c.node('Prior', 'Prior Flow\np_φ(h), φ=θ\n(OOD Check)', shape='component', fillcolor='#ffe0b2')
        c.node('Projector', 'Gradient Descent\nmin(L_OOD + L_flow)', shape='diamond', fillcolor='#ffccbc')
        c.node('h_hat', 'Projected Embedding\nĥ', shape='ellipse', style='filled, bold', fillcolor='#ffab91')
        
        # Edges internal to embedding
        c.edge('Encoder', 'h')
        c.edge('h', 'Prior')
        c.edge('h', 'Projector')
        c.edge('Prior', 'Projector', label='∇ L_OOD')
        c.edge('Projector', 'h_hat')

    # Context  Generation
    with dot.subgraph(name='cluster_context') as c:
        c.attr(label='Context  Generation', style='invis')
        c.node('ContextNet', 'Context Network\ng_ω', shape='component', fillcolor='#dcedc8')
        c.node('Context', 'Context Vector\nC', shape='ellipse', fillcolor='#dcedc8')

    # Trajectory Sampling
    with dot.subgraph(name='cluster_flow') as c:
        c.attr(label='Trajectory Sampling', style='invis')
        c.node('Noise', 'Σ_c ->\nGaussian Noise', shape='eclipse', fillcolor='#f3e5f5')
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
