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
        c.node('State', 'Start x0, Goal xG\nCost Params (rho)', shape='ellipse', fillcolor='#e1f5fe')

    # --- ALGORITHM 3: PROJECTION LOOP (OUTER) ---
    with dot.subgraph(name='cluster_projection') as c:
        c.attr(label='ALGORITHM 3: Projection Loop\n(Outer Loop: n=1 to N)', color='purple', style='rounded,bold')
        
        # VAE Encoder
        c.node('Encoder', 'VAE Encoder\nq_theta(h|E)', shape='component', fillcolor='#fff9c4')
        c.node('h_init', 'h^n (Latent)', shape='ellipse', fillcolor='#fff9c4')
        
        # Prior OOD Check
        c.node('Prior', 'Prior Flow p_phi(h)\nLog Probability Computation\n(Algorithm 3, Line 3)', 
               shape='component', fillcolor='#ffe0b2', style='filled,bold')
        
        # Cost Context
        c.node('CostNet', 'Cost Network g_omega\n(Algorithm 3, Line 4)', shape='component', fillcolor='#ffccbc')
        c.node('Cost_C', 'Cost C=g_omega(x0,xG,h^n)', shape='ellipse', fillcolor='#ffccbc')
        
        # Loss initialization
        c.node('LossInit', 'Loss Init\nL = -log p_phi(h^n)\n(Algorithm 3, Line 6)', 
               shape='box', fillcolor='#ffccbc')
        
        # Internal edges
        c.edge('Encoder', 'h_init')
        c.edge('h_init', 'Prior', label='OOD Check')
        c.edge('h_init', 'CostNet')
        c.edge('CostNet', 'Cost_C')
        c.edge('Prior', 'LossInit', label='Log Prob')

    # --- ALGORITHM 3: SAMPLING LOOP (MIDDLE) ---
    with dot.subgraph(name='cluster_sampling') as c:
        c.attr(label='ALGORITHM 3: Sampling Loop\n(Middle Loop: k=1 to K)\nEach sample evaluated by Algorithm 1', 
               color='blue', style='rounded,bold')
        
        # Noise sampling
        c.node('NoiseSample', 'Sample Noise\nepsilon_k ~ N(0, Sigma_c)\n(Algorithm 3, Line 5)', 
               shape='box', fillcolor='#b3e5fc')
        
        # Get trajectory sample
        c.node('TrajSample', 'Get Sample\nU_k = C + epsilon_k\n(Algorithm 3, Line 5)', 
               shape='box', fillcolor='#b3e5fc')
        
        # Separator
        c.node('Algo1Call', '*** CALL ALGORITHM 1: FlowMPPI ***\n(Evaluate this sample)', 
               shape='component', fillcolor='#ffcccc', style='filled,bold')

    # --- ALGORITHM 1: MPC INNER LOOP ---
    with dot.subgraph(name='cluster_algo1') as c:
        c.attr(label='ALGORITHM 1: FlowMPPI Loop\n(Inner Loop: t=1 to T and j=1 to K_mpc)\nMPC Trajectory Optimization', 
               color='darkgreen', style='rounded,bold')
        
        c.node('Nominal', 'Previous Nominal Trajectory\nU (or initialized from U_k)', 
               shape='box', fillcolor='#c8e6c9')
        
        c.node('MPC_outer', 'For t=1 to T-1:', shape='plain', fontsize='10')
        
        # Time step loop
        c.node('Sample_perturb', 'Sample Perturbation\nepsilon_t ~ N(0, Sigma)\n(Algo 1, Line 5)', 
               shape='box', fillcolor='#c8e6c9')
        
        c.node('Sample_j_loop', 'For j=1 to K:', shape='plain', fontsize='10')
        
        c.node('Generate_sample', 'Generate Sample\ne_t,j ~ N(0, I)\nU_t,j = U_t-1 + e_t,j\n(Algo 1, Line 8-9)', 
               shape='box', fillcolor='#a5d6a7')
        
        c.node('Compute_traj', 'Compute Trajectory\ntau_j ~ p(tau|U_t,j)\n(Algo 1, Line 10)', 
               shape='box', fillcolor='#a5d6a7')
        
        c.node('Compute_cost', 'Compute Cost\nS_j = J(tau_j) + lambda*u\'*Sigma^-1*e\n(Algo 1, Line 11-12)', 
               shape='box', fillcolor='#a5d6a7')
        
        # CEM or MPPI weights
        c.node('Weights', 'Compute Weights\nw_j (MPPI formula)\n(Algo 1, Line 22)', 
               shape='box', fillcolor='#81c784')
        
        # Update trajectory
        c.node('Update_traj', 'Update Nominal\nU_new = sum(w_j * U_t,j)\n(Algo 1, Line 23)', 
               shape='box', fillcolor='#81c784')
        
        # Return
        c.node('Algo1_return', 'Return Evaluated U\n(Algo 1, Line 24)', 
               shape='component', fillcolor='#7cb342', style='filled,bold')
        
        # Internal edges for Algo 1
        c.edge('Nominal', 'MPC_outer')
        c.edge('MPC_outer', 'Sample_perturb')
        c.edge('Sample_perturb', 'Sample_j_loop')
        c.edge('Sample_j_loop', 'Generate_sample')
        c.edge('Generate_sample', 'Compute_traj')
        c.edge('Compute_traj', 'Compute_cost')
        c.edge('Compute_cost', 'Weights')
        c.edge('Weights', 'Update_traj')
        c.edge('Update_traj', 'Algo1_return')

    # --- BACK TO ALGORITHM 3: WEIGHT & LOSS ACCUMULATION ---
    with dot.subgraph(name='cluster_loss') as c:
        c.attr(label='ALGORITHM 3: Weight & Loss Accumulation\n(Back to Line 8-9)', 
               color='orange', style='rounded,bold')
        
        c.node('Weight_k', 'Compute Sample Weight\nw_k = Weight(U_k, C, h)\n(Algo 3, Line 8, Eq 11)', 
               shape='box', fillcolor='#ffe082')
        
        c.node('Accum_loss', 'Accumulate Loss\nL = L - w_k*log q_C(U_k|C, h^n)\n(Algo 3, Line 9)', 
               shape='box', fillcolor='#ffe082')

    # --- GRADIENT UPDATE ---
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
    dot.edge('Cost_C', 'NoiseSample', label='For k=1 to K')
    dot.edge('NoiseSample', 'TrajSample')
    
    # 4. Call Algorithm 1
    dot.edge('TrajSample', 'Algo1Call', label='Pass U_k')
    dot.edge('Algo1Call', 'Nominal', label='*** CALL ALGO 1 ***')
    
    # 5. Algorithm 1 processes
    dot.edge('Algo1_return', 'Weight_k', label='Return evaluated U_k', color='darkgreen', style='bold')
    
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
    print("Corrected block diagram generated as 'flow_mpc_diagram_algo1_algo3.png'")
    print("\nKey improvements:")
    print("1. ✓ Clear nested loop structure (3 levels)")
    print("2. ✓ Explicit Algorithm 1 call within Algorithm 3 sampling loop")
    print("3. ✓ MPC trajectory evaluation shown in detail")
    print("4. ✓ Algorithm 3 line numbers labeled")
    print("5. ✓ Weight and loss computation properly positioned")
    print("6. ✓ Gradient update and h optimization shown")

if __name__ == "__main__":
    create_mpc_block_diagram()
