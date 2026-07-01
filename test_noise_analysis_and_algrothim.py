import unittest
import numpy as np
import qutip as qt

# Import our custom modules
from deutsch_jozsa import create_dj_oracle, create_dynamic_oracle
from noise_channels import bitflip_channel, phaseflip_channel, depolarizing_channel
from deutch_jozsa_noisy import run_noisy_dj

class TestFaultToleranceAndNoise(unittest.TestCase):
    
    def test_oracle_generation(self):
        """Test that Unitary Oracles are mathematically sound."""
        n = 3
        # 1. Constant Oracle should be the Identity matrix (or negative Identity)
        U_const = create_dj_oracle(n, "constant_0")
        self.assertTrue(np.allclose(U_const.full(), np.eye(2**n)), "Constant_0 should be Identity.")
        self.assertTrue(U_const.isunitary, "Oracle must be unitary.")  # FIXED HERE
        
        # 2. Balanced Oracle should have a Trace of 0 (equal +1 and -1 phases)
        U_bal = create_dj_oracle(n, "balanced")
        self.assertAlmostEqual(U_bal.tr(), 0.0, msg="Balanced oracle trace must be 0.")
        self.assertTrue(U_bal.isunitary, "Oracle must be unitary.")    # FIXED HERE
        
        # 3. Dynamic Function vs Static String matching
        def mock_balanced_function(bit_string):
            return sum(bit_string) % 2
            
        U_dyn = create_dynamic_oracle(n, mock_balanced_function)
        self.assertTrue(np.allclose(U_bal.full(), U_dyn.full()), "Dynamic Parity should match static 'balanced' string.")
    
    def test_noise_channels(self):
        """Test that Kraus operators obey physical laws."""
        # Start with |0> state for 1 qubit
        rho_0 = qt.basis(2, 0) * qt.basis(2, 0).dag()
        
        # 1. Bitflip at p=1.0 should turn |0><0| into |1><1|
        rho_flipped = bitflip_channel(rho_0, p=1.0, target=0)
        expected_1 = qt.basis(2, 1) * qt.basis(2, 1).dag()
        self.assertTrue(np.allclose(rho_flipped.full(), expected_1.full()), "100% Bitflip failed.")
        self.assertAlmostEqual(rho_flipped.tr(), 1.0, msg="Bitflip must preserve trace.")
        
        # 2. Phaseflip at p=1.0 on |+> should turn it into |->
        psi_plus = (qt.basis(2, 0) + qt.basis(2, 1)).unit()
        rho_plus = psi_plus * psi_plus.dag()
        rho_phase_flipped = phaseflip_channel(rho_plus, p=1.0, target=0)
        
        psi_minus = (qt.basis(2, 0) - qt.basis(2, 1)).unit()
        expected_minus = psi_minus * psi_minus.dag()
        self.assertTrue(np.allclose(rho_phase_flipped.full(), expected_minus.full()), "100% Phaseflip failed on |+>.")
        self.assertAlmostEqual(rho_phase_flipped.tr(), 1.0, msg="Phaseflip must preserve trace.")
        
        # 3. Global Depolarizing at p=1.0 should result in the maximally mixed state I/d
        n = 2
        rho_n2 = qt.tensor([qt.basis(2,0)] * n) * qt.tensor([qt.basis(2,0)] * n).dag()
        rho_depol = depolarizing_channel(rho_n2, p=1.0)
        expected_mixed = qt.qeye(2**n) / (2**n)
        self.assertTrue(np.allclose(rho_depol.full(), expected_mixed.full()), "100% Depolarizing failed to reach I/d.")
        self.assertAlmostEqual(rho_depol.tr(), 1.0, msg="Depolarizing must preserve trace.")

    def test_dj_algorithm_density_matrix_engine(self):
        """Test the integration of the algorithm engine under noise."""
        n = 3
        
        # 1. Base case: Noiseless (p=0) Constant function -> should measure |000> exactly 100% of the time
        prob_const = run_noisy_dj(n, "constant_0", noise_prob=0.0)
        self.assertAlmostEqual(prob_const, 1.0, msg="Noiseless Constant function failed to reach 100%.")
        
        # 2. Base case: Noiseless (p=0) Balanced function -> should measure |000> exactly 0% of the time
        prob_bal = run_noisy_dj(n, "balanced", noise_prob=0.0)
        self.assertAlmostEqual(prob_bal, 0.0, msg="Noiseless Balanced function failed to reach 0%.")
        
        # 3. Extreme Noise: 100% Depolarizing (post_oracle) -> should guess |000> exactly 1/8th (12.5%) of the time
        prob_depol = run_noisy_dj(n, "constant_0", depolarizing_channel, noise_prob=1.0, noise_loc="post_oracle")
        self.assertAlmostEqual(prob_depol, 1/(2**n), msg="Algorithm failed depolarizing asymptote check.")
        
        # 4. Keyword Routing check: Applying Bitflip at 'pre_H1' should destroy Constant algorithm
        prob_pre_h1 = run_noisy_dj(n, "constant_0", bitflip_channel, noise_prob=1.0, noise_loc="pre_H1")
        self.assertAlmostEqual(prob_pre_h1, 0.0, msg="Pre-H1 Bitflip failed to destroy algorithm.")
        
if __name__ == '__main__':
    unittest.main(verbosity=2)