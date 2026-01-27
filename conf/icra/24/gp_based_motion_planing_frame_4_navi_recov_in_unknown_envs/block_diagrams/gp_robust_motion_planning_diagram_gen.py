from graphviz import Digraph

def create_gp_motion_planning_diagram():
    dot = Digraph(comment='GP-based Robust Motion Planning Framework', format='png')
    dot.attr(rankdir='LR', splines='ortho', compound='true')
    
    # Global styles
    dot.attr('node', shape='box', style='filled', fillcolor='white', fontname='Helvetica', fontsize='11')
    dot.attr('edge', fontname='Helvetica', fontsize='9')

    # --- OFFLINE STAGE ---
    with dot.subgraph(name='cluster_offline') as c:
        c.attr(label='Offline Stage', style='filled', color='#bbdefb', fillcolor='#e3f2fd')
        
        # Simulation Data
        c.node('SimData', 'Simulated Data\n(fr. "Forest World")\n{stat x, \nCorridor C (constraint), \nSuccess/Fail}', 
               shape='cylinder', fillcolor='#b3e5fc')
        
        # GP Training
        c.node('GPTrain', 'GP Training\nfor\nSolver Failure Detection', 
               shape='component', fillcolor='#81d4fa')
        
        # Internal Edge
        c.edge('SimData', 'GPTrain', label='D (features), \nP (values {P(succ/fail)})')

    # --- ONLINE STAGE ---
    with dot.subgraph(name='cluster_online') as c:
        c.attr(label='Online (Inference) Stage', style='filled', color='#c8e6c9', fillcolor='#e8f5e9')

        # --- PLANNING PIPELINE ---
        with c.subgraph(name='cluster_planning') as p:
            p.attr(label='Motion Planner', color='grey', style='dashed')
            
            # Front-End
            p.node('FrontEnd', 'Front-End\nStep-1: JPS Path Planning (in: x(t0); out: path)\nStep-2: Corridor Gen (in: path; out: C)', 
                   shape='component', fillcolor='#cfd8dc')
            
            # Back-End
            p.node('BackEnd', 'Back-End\n(Trajectory Opt)', 
                   shape='component', fillcolor='#cfd8dc')
            
            p.edge('FrontEnd', 'BackEnd', label=' \n\n\n\nState x(t0), Corridor C')

        # --- FAILURE DETECTION ---
        with c.subgraph(name='cluster_detection') as d:
            d.attr(label='Proactive Failure Detection', color='#ffccbc', style='bold')
            
            # GP Fail Detect
            d.node('GPDetect', 'GP Fail Detect: Predict P(Failure)', 
                   shape='box', fillcolor='#ffab91')
            
            # Decision
            d.node('RiskCheck', 'ρ > ψ', 
                   shape='diamond', fillcolor='#ffccbc')
            
            d.edge('GPDetect', 'RiskCheck')

        # --- RECOVERY MODULE ---
        with c.subgraph(name='cluster_recovery') as r:
            r.attr(label='Recovery Behavior', color='#ffcdd2', style='bold')
            
            # GP Recovery Search
            r.node('GPRec', 'GP Recovery\nFind Safe State x_r\n(Sampling-based)', 
                   shape='component', fillcolor='#ef9a9a')

        # --- CONTROLLERS (MPC) ---
        with c.subgraph(name='cluster_control') as ctrl:

            ctrl.attr(label='MPC', color='#546e7a', style='filled', fillcolor='#b0bec5')
            
            # Go-To-Goal MPC (Recovery)
            ctrl.node('GTG_MPC', 'GTG MPC\n(Go-To-Goal)',
                      shape='component', fillcolor='white')
            
            # Tracking MPC (Nominal)
            ctrl.node('Track_MPC', 'τ MPC', 
                      shape='component', fillcolor='white')

        # --- PLANT ---
        c.node('Plant', 'Plant\n(Robot Environment)', shape='doubleoctagon', fillcolor='#a5d6a7')

    # === MAIN CONNECTING EDGES ===

    # 1. Offline to Online (Model Parameters)
    dot.edge('GPTrain', 'GPDetect', label='Model Params', style='dashed')
    dot.edge('GPTrain', 'GPRec', label='Model Params', style='dashed')

    # 2. Planning Flow
    dot.edge('Plant', 'FrontEnd', label='\n\n\n                                                             State x(t0)')
    dot.edge('FrontEnd', 'GPDetect')
    dot.edge('BackEnd', 'Track_MPC', label='\n\nTrajectory τ')

    # 3. Detection Feedback Loop
    dot.edge('GTG_MPC', 'GPDetect', label='{x_i}')

    # 4. Decision Logic
    dot.edge('RiskCheck', 'Track_MPC', label='                           NO')
    dot.edge('RiskCheck', 'GPRec', label='YES\n(Trigger Recovery)\n ')

    # 5. Recovery Flow
    dot.edge('GPRec', 'GTG_MPC', label='Recovery Goal x_r')

    # 6. Control Output to Plant
    # dot.edge('GTG_MPC', 'Plant', label='Control u')

    dot.edge('Track_MPC', 'Plant', label='\n\n\n\n\n\nControl u       ')

    dot.edge('Plant', 'Track_MPC')

    # Render
    dot.render('gp_robust_motion_planning_diagram', view=False, cleanup=True)

if __name__ == "__main__":
    create_gp_motion_planning_diagram()