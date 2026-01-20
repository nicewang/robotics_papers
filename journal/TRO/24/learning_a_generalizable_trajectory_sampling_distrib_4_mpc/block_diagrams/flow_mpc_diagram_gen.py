from graphviz import Digraph

def create_mpc_block_diagram():
    dot = Digraph(comment='FlowMPC Architecture - Algo1+Algo3', format='png')
    dot.attr(rankdir='TB', splines='ortho', compound='true')
    
    # Global styles
    dot.attr('node', shape='box', style='filled', fillcolor='white', fontname='Helvetica', fontsize='11')
    dot.attr('edge', fontname='Helvetica', fontsize='9')

    # --- INPUTS ---
    with dot.subgraph(name='cluster_inputs') as c:
        c.attr(label='System Inputs', style='dashed', color='grey')
        c.node('Env', 'Environment (SDF)\nE', shape='ellipse', fillcolor='#e1f5fe')
        c.node('State', 'Start x0, Goal xG\nCost Params ρ', shape='ellipse', fillcolor='#e1f5fe')

    # --- ALGORITHM 3: PROJECTION LOOP (OUTER) ---
    with dot.subgraph(name='cluster_projection') as c:
        c.attr(label='Algorithm 3: Projection Loop\n(Outer Loop: n=1 to N)', color='purple', style='rounded,bold')
        
        # VAE Encoder
        c.node('Encoder', 'VAE Encoder\nq_θ(h|E)', shape='component', fillcolor='#fff9c4')
        c.node('h_init', 'Latent h^n', shape='ellipse', fillcolor='#fff9c4')
        
        # Prior Flow and OOD Check
        c.node('Prior', 'Prior Flow\np_φ(h), φ=θ\nOOD Check', shape='component', fillcolor='#ffe0b2')
        
        # Cost Context
        c.node('CostNet', 'Context net g_ω\n(Cost Context)', shape='component', fillcolor='#ffccbc')
        c.node('Cost_C', 'Cost C=g_ω(x0,xG,h^n)', shape='ellipse', fillcolor='#ffccbc')
        
        # Loss Initialization
        c.node('LossInit', 'Loss Init\nL = -p_φ(h^n)', shape='ellipse', fillcolor='#ffe0b2')
        
        # Internal Edges
        c.edge('h_init', 'Prior')
        c.edge('h_init', 'CostNet')
        c.edge('CostNet', 'Cost_C')
        c.edge('Prior', 'LossInit')

    # --- ALGORITHM 3: SAMPLING LOOP (INNER) ---
    with dot.subgraph(name='cluster_sampling') as c:
        c.attr(label='Algorithm 3: Sampling Loop\n(Inner Loop: k=1 to K)\nEach sample evaluated by FlowMPPI', 
               color='blue', style='rounded,bold')
        
        # Noise sampling
        c.node('NoiseSample', 'Sample Noise\nΣ -> Noise', 
               shape='component', fillcolor='#b3e5fc')
        
        # Get Trajectory Samples
        c.node('TrajSample', 'Sample Trajectory U\nLoop: for k from 1 to K', 
               shape='component', fillcolor='#b3e5fc')
        
        # Call for Algorithm 1
        c.node('Algo1Call', '*** Call Algorithm 1: FlowMPPI ***\n(Evaluate sampled trajectories)', 
               shape='component', fillcolor='#ffcccc')

    # --- ALGORITHM 1: MPC LOOP (INNER) ---
    with dot.subgraph(name='cluster_algo1') as c:
        c.attr(label='Algorithm 1: FlowMPPI Loop\n(Inner Loop: k=1 to K)\nMPC Trajectory Optimization', 
               color='darkgreen', style='rounded,bold')
        
        c.node('Nominal', '*** Requested from Algorithm 3: Projection ***', 
               shape='component', fillcolor='#c8e6c9')
        
        # Shift Operation
        c.node('shift_opera', 'Shift Operation\nU_t-1 <- U_t\nU_T-1 ~ N(0, Σ)\nLoop: for t from 1 to T-1', 
               shape='component', fillcolor='#a5d6a7')
        
        # Generate Samples
        c.node('gen_sample_1', 'Generate samples by\nperturbing nominal U\nLoop: for k from 1 to K/2', 
               shape='component', fillcolor='#a5d6a7')
        
        c.node('gen_sample_2', 'Generate samples from\ncontrol sequence posterior\nLoop: for k from K/2+1 to K', 
               shape='component', fillcolor='#a5d6a7')
        
        c.node('u_', 'U_', shape='ellipse', fillcolor='#a5d6a7')
        
        # Update U
        c.node('compute_new_u', 'Compute new nominal U', 
               shape='component', fillcolor='#81c784')
        
        # Return
        c.node('Algo1_return', 'Return Evaluated U', 
               shape='component', fillcolor='#7cb342')
        
        # Internal edges
        c.edge('Nominal', 'shift_opera', label='U')
        c.edge('shift_opera', 'gen_sample_1')
        c.edge('shift_opera', 'gen_sample_2')
        c.edge('gen_sample_1', 'u_')
        c.edge('gen_sample_2', 'u_')
        c.edge('u_', 'compute_new_u')
        c.edge('compute_new_u', 'Algo1_return', label='U_new')

    # --- BACK TO ALGORITHM 3: WEIGHT & LOSS ACCUMULATION (INNER LOOP) ---
    with dot.subgraph(name='cluster_loss') as c:

        c.attr(label='Algorithm 3: Weight & Loss Accumulation\n(Inner Loop: k=1 to K)', 
               color='orange', style='rounded,bold')
        
        # Weights Sum
        c.node('Weight', 'Compute Sample Weights\nw_k for k=1 to K (Loop))', 
               shape='box', fillcolor='#ffe082')
        
        # Loss Accumulation
        c.node('Accum_loss', 'Accumulate Loss\nL = L - w_k*log q(U_k|C)\nLoop: k=1 to K', 
               shape='box', fillcolor='#ffe082')

    # --- GRADIENT DSCENT ---
    with dot.subgraph(name='cluster_gradient') as c:

        c.attr(label='Algorithm 3: Gradient Descent', 
               color='red', style='rounded,bold')
        
        c.node('Gradient', 'Compute Gradient\ndL/dh', 
               shape='component', fillcolor='#ffab91')
        
        c.node('Update_h', 'Update Latent\nh^(n+1) = h^n - η*dL/dh', 
               shape='component', fillcolor='#ff7043')

    # --- ITERATION DECISION ---
    c.node('LoopCheck', 'Finished or Not', shape='diamond', fillcolor='#ffccbc')

    # --- FINAL OUTPUT ---
    dot.node('OptimalControl', 'Return\nGeneralizable Trajectories\nU*', shape='doubleoctagon', 
            fillcolor='#c8e6c9')

    # === MAIN CONNECTING EDGES ===
    
    # 1. Input to Encoder & CostNet
    dot.edge('Env', 'Encoder')
    dot.edge('State', 'CostNet')
    
    # 2. Algorithm 3 Setup
    dot.edge('Encoder', 'h_init')
    
    # 3. Sampling Loop Begins
    dot.edge('Cost_C', 'TrajSample')
    dot.edge('NoiseSample', 'TrajSample', label='noise')
    
    # 4. Call Algorithm 1
    dot.edge('TrajSample', 'Algo1Call', label='U')
    dot.edge('Algo1Call', 'Nominal', label='*** CALL ALGO 1 ***')
    
    # 5. Back to Algo 3
    dot.edge('Algo1_return', 'Weight', label='Return updated U_new')
    dot.edge('Weight', 'Accum_loss', label='w_k')
    dot.edge('LossInit', 'Accum_loss')
    
    # 6. Compute Gradient
    dot.edge('Accum_loss', 'Gradient', label='After all k=1:K')
    
    # 7. Gradient Descent
    dot.edge('Gradient', 'Update_h')
    dot.edge('Update_h', 'LoopCheck')
    
    # 8. Loop Back
    dot.edge('LoopCheck', 'h_init', label='Not finish yet')
    dot.edge('LoopCheck', 'OptimalControl', label='Done')
#     dot.edge('Algo1_return', 'OptimalControl')
    
    # Render
    dot.render('flow_mpc_diagram', view=False, cleanup=True)

if __name__ == "__main__":
    create_mpc_block_diagram()
