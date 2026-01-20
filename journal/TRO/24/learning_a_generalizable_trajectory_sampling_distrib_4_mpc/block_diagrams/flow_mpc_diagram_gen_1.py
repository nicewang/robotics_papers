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
        
        # Prior OOD Check
        c.node('Prior', 'Prior Flow\np_φ(h), φ=θ\nOOD Check', shape='component', fillcolor='#ffe0b2')
        
        # Cost Context
        c.node('CostNet', 'Context net g_ω\n(Cost Context)', shape='component', fillcolor='#ffccbc')
        c.node('Cost_C', 'Cost C=g_ω(x0,xG,h^n)', shape='ellipse', fillcolor='#ffccbc')
        
        # Loss initialization
        c.node('LossInit', 'Loss Init\nL = -p_φ(h^n)', shape='ellipse', fillcolor='#ffe0b2')
        
        # Internal edges
        c.edge('h_init', 'Prior')
        c.edge('h_init', 'CostNet')
        c.edge('CostNet', 'Cost_C')
        c.edge('Prior', 'LossInit')

    # --- ALGORITHM 3: SAMPLING LOOP (MIDDLE) ---
    with dot.subgraph(name='cluster_sampling') as c:
        c.attr(label='Algorithm 3: Sampling Loop\n(Inner Loop: k=1 to K)\nEach sample evaluated by FlowMPPI', 
               color='blue', style='rounded,bold')
        
        # Noise sampling
        c.node('NoiseSample', 'Sample Noise\nΣ -> Noise', 
               shape='component', fillcolor='#b3e5fc')
        
        # Get trajectory sample
        c.node('TrajSample', 'Sample Trajectory U\nLoop: for k from 1 to K', 
               shape='component', fillcolor='#b3e5fc')
        
        # Separator
        c.node('Algo1Call', '*** Call Algorithm 1: FlowMPPI ***\n(Evaluate sampled trajectories)', 
               shape='component', fillcolor='#ffcccc')

    # --- ALGORITHM 1: MPC INNER LOOP ---
    with dot.subgraph(name='cluster_algo1') as c:
        c.attr(label='ALGORITHM 1: FlowMPPI Loop\n(Inner Loop: k=1 to K)\nMPC Trajectory Optimization', 
               color='darkgreen', style='rounded,bold')
        
        c.node('Nominal', '*** Requested from Algorithm 3: Projection ***', 
               shape='component', fillcolor='#c8e6c9')
        
        # Time step loop
        c.node('shift_opera', 'Shift Operation\nU_t-1 <- U_t\nU_T-1 ~ N(0, Σ)\nLoop: for t from 1 to T-1', 
               shape='component', fillcolor='#a5d6a7')
        
        c.node('gen_sample_1', 'Generate samples by\nperturbing nominal U\nLoop: for k from 1 to K/2', 
               shape='component', fillcolor='#a5d6a7')
        
        c.node('gen_sample_2', 'Generate samples from\ncontrol sequence posterior\nLoop: for k from K/2+1 to K', 
               shape='component', fillcolor='#a5d6a7')
        
        c.node('u_', 'U_', shape='ellipse', fillcolor='#a5d6a7')
        
        # iCEM or MPPI weights
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

    # --- BACK TO ALGORITHM 3: WEIGHT & LOSS ACCUMULATION ---
    with dot.subgraph(name='cluster_loss') as c:
        c.attr(label='ALGORITHM 3: Weight & Loss Accumulation\n(Back to Line 8-9)', 
               color='orange', style='rounded,bold')
        
        c.node('Weight_k', 'Compute Sample Weight\nw_k = Weight(U_k, C, h)\n(Algo 3, Line 8, Eq 11)', 
               shape='box', fillcolor='#ffe082')
        
        c.node('Accum_loss', 'Accumulate Loss\nL = L - w_k*log q_C(U_k|C, h^n)\n(Algo 3, Line 9)', 
               shape='box', fillcolor='#ffe082')

    # --- GRADIENT DSCENT ---
    with dot.subgraph(name='cluster_gradient') as c:
        c.attr(label='ALGORITHM 3: Gradient Update\n(Line 10)', 
               color='red', style='rounded,bold')
        
        c.node('Gradient', 'Compute Gradient\ndL/dh = -dlog p_phi(h)/dh - sum(w_k*dlog q_C/dh)\n(Algo 3, Line 10)', 
               shape='box', fillcolor='#ffab91')
        
        c.node('Update_h', 'Update Latent\nh^(n+1) = h^n - eta*dL/dh\n(Algo 3, Line 10)', 
               shape='box', fillcolor='#ff7043', style='filled,bold')

    # --- ITERATION DECISION ---
    c.node('LoopCheck', 'n < N?', shape='diamond', fillcolor='#ffccbc')

    # --- FINAL OUTPUT ---
    dot.node('OptimalControl', 'Optimal Control Sequence\nU_star', shape='doubleoctagon', 
            fillcolor='#c8e6c9', style='filled,bold')

    # === MAIN CONNECTING EDGES ===
    
    # 1. Input to Encoder
    dot.edge('Env', 'Encoder')
    dot.edge('State', 'CostNet')
    
    # 2. Algorithm 3 Setup
    dot.edge('Encoder', 'h_init')
    
    # 3. Sampling Loop begins
    dot.edge('Cost_C', 'TrajSample')
    dot.edge('NoiseSample', 'TrajSample', label='noise')
    
    # 4. Call Algorithm 1
    dot.edge('TrajSample', 'Algo1Call', label='U')
    dot.edge('Algo1Call', 'Nominal', label='*** CALL ALGO 1 ***')
    
    # 5. Algorithm 1 processes
    dot.edge('Algo1_return', 'Weight_k', label='Return updated U_new')
    
    # 6. Back to Algo 3
    dot.edge('Weight_k', 'Accum_loss')
    
    # 7. All K samples processed, compute gradient
    dot.edge('Accum_loss', 'Gradient', label='After all k=1:K')
    
    # 8. Gradient update
    dot.edge('Gradient', 'Update_h')
    dot.edge('Update_h', 'LoopCheck')
    
    # 9. Loop back
    dot.edge('LoopCheck', 'h_init', label='Yes (n+1)', constraint='false', style='dashed')
    dot.edge('LoopCheck', 'OptimalControl', label='No (Done)')
    
    # Render
    dot.render('flow_mpc_diagram_algo1_algo3', view=False, cleanup=True)

if __name__ == "__main__":
    create_mpc_block_diagram()
