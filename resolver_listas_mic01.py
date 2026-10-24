#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIC 01 - Física de Dispositivos Semicondutores
Script de Resolução Completa e Verificação Numérica: Lista 2 e Lista 3
Baseado nas equações e constantes dos Slides (Aulas 8 a 14) e do livro Kanaan Kano.
"""

import math


def banner(titulo: str) -> None:
    print("\n" + "=" * 78)
    print(f"  {titulo}")
    print("=" * 78)


def resolver_lista_2() -> None:
    banner("LISTA DE EXERCÍCIOS 2 — JUNÇÃO PN (Aulas 8 a 13 & Kanaan Kano Caps. 5 e 7)")

    # Constantes fundamentais (Aula 11 Slide 6 / Aula 14 Slide 19 / Kanaan Kano Apêndice B)
    q = 1.6e-19            # Carga elementar [C]
    k_J = 1.3806e-23       # Constante de Boltzmann [J/K] (Aula 11 Slide 6 / Aula 14 Slide 19)
    k_eV = 8.6173e-5       # Constante de Boltzmann [eV/K] (Aula 14 Slide 19)
    T = 300.0              # Temperatura [K]
    Vt_exato = (k_J * T) / q      # ~ 0.025886 V (usando k e q da Aula 11 Slide 6)
    Vt_lista3 = 8.62e-5 * T       # = 0.025860 V (usando k da Lista 3 pág. 2)
    Vt_slide19 = 0.026            # = 0.026000 V (valor arredondado na Aula 14 Slide 19)

    # -------------------------------------------------------------------------
    # QUESTÃO 1 (Problema 5.3 do Kanaan Kano)
    # -------------------------------------------------------------------------
    print("\n--- QUESTÃO 1 (Lista 2) ---")
    rho_n = 1.0     # Ohm.cm
    rho_p = 0.1     # Ohm.cm
    mu_p = 1700.0   # cm^2/(V.s)
    mu_n = 3600.0   # cm^2/(V.s) (No enunciado impresso há typo "mu_p = 3600", mas em Ge mu_n = 3600 e mu_p = 1700)
    ni_1 = 2.5e13   # cm^-3 ( Germânio a 300 K )

    # Da relação de resistividade (Kanaan Kano Eq. 4.19 / Aula 8):
    # rho_n = 1 / (q * mu_n * N_D)  e  rho_p = 1 / (q * mu_p * N_A)
    ND_1 = 1.0 / (q * mu_n * rho_n)
    NA_1 = 1.0 / (q * mu_p * rho_p)

    # Da Aula 9 Slide 4: V_bi = (kT/q) * ln( (N_A * N_D) / n_i^2 )
    Vbi_1_2586 = Vt_lista3 * math.log((NA_1 * ND_1) / (ni_1 ** 2))
    Vbi_1_2589 = Vt_exato * math.log((NA_1 * ND_1) / (ni_1 ** 2))
    Vbi_1_2600 = Vt_slide19 * math.log((NA_1 * ND_1) / (ni_1 ** 2))

    print(f"Concentração de doadores (lado N):   N_D = 1 / (q * mu_n * rho_n) = {ND_1:.4e} cm^-3")
    print(f"Concentração de aceitadores (lado P): N_A = 1 / (q * mu_p * rho_p) = {NA_1:.4e} cm^-3")
    print(f"Produto N_A * N_D = {NA_1 * ND_1:.4e} cm^-6 (invariante à troca entre mu_n e mu_p!)")
    print(f"Built-in voltage V_bi (com kT/q = 0,02586 V): V_bi = {Vbi_1_2586:.4f} V (~ 0,298 V)")
    print(f"Built-in voltage V_bi (com kT/q = 0,02589 V): V_bi = {Vbi_1_2589:.4f} V (~ 0,299 V)")
    print(f"Built-in voltage V_bi (com kT/q = 0,02600 V): V_bi = {Vbi_1_2600:.4f} V (~ 0,300 V)")

    # -------------------------------------------------------------------------
    # QUESTÃO 2 (Baseada no Problema 5.7 do Kanaan Kano)
    # -------------------------------------------------------------------------
    print("\n--- QUESTÃO 2 (Lista 2) ---")
    ND_2 = 1.0e18        # cm^-3 (região N+)
    NA_2 = 1.0e16        # cm^-3 (região P)
    A_2 = 1.2e-4         # cm^2
    tau_p = 1.0e-6       # s
    tau_n = 1.0e-6       # s
    eps_r = 11.7
    eps_0_m = 8.854e-12  # F/m
    eps_0_cm = 8.854e-14 # F/cm
    eps_s_cm = eps_r * eps_0_cm  # 1.035918e-12 F/cm
    Dn = 34.0            # cm^2/s (elétrons na região P)
    Dp = 13.0            # cm^2/s (lacunas na região N)
    ni_2 = 1.0e10        # cm^-3

    # Comprimentos de difusão (Aula 11 Slide 2: L_p = sqrt(D_p * tau_p), L_n = sqrt(D_n * tau_n))
    Lp = math.sqrt(Dp * tau_p)
    Ln = math.sqrt(Dn * tau_n)

    # Portadores minoritários no equilíbrio (Aula 8 Slide 1 / Aula 12 Slide 6):
    p0n = (ni_2 ** 2) / ND_2
    n0p = (ni_2 ** 2) / NA_2

    # a) Corrente reversa de saturação I_S (Aula 11 Slide 6 / Aula 12 Slide 6):
    # I_S = A * q * [ (D_p * p_0n / L_p) + (D_n * n_0p / L_n) ]
    termo_lacunas = (Dp * p0n) / Lp
    termo_eletrons = (Dn * n0p) / Ln
    Is_completo = A_2 * q * (termo_lacunas + termo_eletrons)
    Is_unilateral = A_2 * q * termo_eletrons  # Aproximação n+p (N_D >> N_A)

    print(f"L_p = sqrt(D_p * tau_p) = {Lp:.4e} cm ({Lp * 1e4:.2f} um)")
    print(f"L_n = sqrt(D_n * tau_n) = {Ln:.4e} cm ({Ln * 1e4:.2f} um)")
    print(f"p_0n = n_i^2 / N_D = {p0n:.2e} cm^-3 | n_0p = n_i^2 / N_A = {n0p:.2e} cm^-3")
    print(f"a) I_S (expressão completa)    = {Is_completo:.4e} A (~ 1,13 fA)")
    print(f"   I_S (aprox. unilateral n+p) = {Is_unilateral:.4e} A (~ 1,12 fA)")

    # b) Corrente para polarização direta V_a = +0,5 V (Aula 11 Slide 6):
    # I = I_S * [ exp(q * V_a / kT) - 1 ]
    Va_dir = 0.5
    I_dir_2586 = Is_completo * (math.exp(Va_dir / Vt_lista3) - 1.0)
    I_dir_2589 = Is_completo * (math.exp(Va_dir / Vt_exato) - 1.0)
    I_dir_2600 = Is_completo * (math.exp(Va_dir / Vt_slide19) - 1.0)
    print(f"b) Para V_a = +0,5 V (polarização direta):")
    print(f"   I (com kT/q = 0,02586 V) = {I_dir_2586:.4e} A (~ 0,281 uA)")
    print(f"   I (com kT/q = 0,02589 V) = {I_dir_2589:.4e} A (~ 0,275 uA)")
    print(f"   I (com kT/q = 0,02600 V) = {I_dir_2600:.4e} A (~ 0,253 uA)")

    # c) Corrente para polarização reversa V_a = -0,5 V:
    Va_rev = -0.5
    I_rev = Is_completo * (math.exp(Va_rev / Vt_lista3) - 1.0)
    print(f"c) Para V_a = -0,5 V (polarização reversa):")
    print(f"   Como exp(-0,5 / 0,02586) = {math.exp(Va_rev / Vt_lista3):.3e} << 1, temos I = -I_S:")
    print(f"   I = {I_rev:.4e} A (~ -1,13 x 10^-15 A)")

    # d) Largura da zona de depleção com polarização reversa V_a = -0,5 V (Aula 10 Slide 3):
    # W = sqrt( (2 * eps_s / q) * ((N_A + N_D) / (N_A * N_D)) * (V_bi - V_a) )
    Vbi_2_2586 = Vt_lista3 * math.log((NA_2 * ND_2) / (ni_2 ** 2))
    Vbi_2_2600 = Vt_slide19 * math.log((NA_2 * ND_2) / (ni_2 ** 2))
    Vj_2 = Vbi_2_2586 - Va_rev  # V_bi - (-0.5) = V_bi + 0.5
    W_completo = math.sqrt(((2.0 * eps_s_cm) / q) * ((NA_2 + ND_2) / (NA_2 * ND_2)) * Vj_2)
    W_unilateral = math.sqrt(((2.0 * eps_s_cm) / (q * NA_2)) * Vj_2)
    print(f"d) V_bi = {Vbi_2_2586:.4f} V (ou {Vbi_2_2600:.4f} V com Vt=0,026 V)")
    print(f"   V_j = V_bi - V_a = {Vbi_2_2586:.4f} - (-0,5) = {Vj_2:.4f} V")
    print(f"   W (fórmula completa)   = {W_completo:.4e} cm = {W_completo * 1e4:.4f} um (~ 418 nm)")
    print(f"   W (aprox. unilateral)  = {W_unilateral:.4e} cm = {W_unilateral * 1e4:.4f} um (~ 416 nm)")

    # -------------------------------------------------------------------------
    # QUESTÃO 3 (Lista 2)
    # -------------------------------------------------------------------------
    print("\n--- QUESTÃO 3 (Lista 2) ---")
    # Pela Aula 8 Slide 3 (phi = -int E dx) e Aula 9 Slide 7 (V_bi = -E_max * W / 2):
    # O potencial através da zona de depleção é dado pela área do triângulo do perfil de campo elétrico!
    # No painel central (equilíbrio):
    #   E_max,0 = -16 kV/cm = -1,6 x 10^4 V/cm
    #   Pela escala do eixo horizontal (cada divisão entre traços vale 1 um):
    #   A largura da zona de depleção no equilíbrio (da junção até x'=0) ocupa 1 divisão: W_0 = 1 um = 10^-4 cm.
    #   Logo, V_bi = -E_max,0 * W_0 / 2 = (16 x 10^3 V/cm) * (10^-4 cm) / 2 = 0,80 V.
    # No último painel (polarizado):
    #   E_max = -8 kV/cm = -0,8 x 10^4 V/cm (metade do campo no equilíbrio!).
    #   Na aproximação de depleção (Aula 9 Slide 5: |E_max| = q * N_D * x_n / eps), a largura W = x_n é
    #   diretamente proporcional a |E_max|. Como |E_max| caiu pela metade, W também cai pela metade:
    #   W = 0,5 um = 0,5 x 10^-4 cm (exatamente meia divisão vista no último painel!).
    #   Logo, a nova barreira de potencial na junção (Aula 10 Slide 3: V_j = V_bi - V_a) é a área do novo triângulo:
    #   V_j = V_bi - V_a = -E_max * W / 2 = (8 x 10^3 V/cm) * (0,5 x 10^-4 cm) / 2 = 0,20 V.
    #   Portanto: V_a = V_bi - V_j = 0,80 V - 0,20 V = +0,60 V (Polarização Direta, pois W e |E_max| diminuíram!).
    Emax_eq = -16e3    # V/cm
    W_eq = 1.0e-4      # cm (1 um)
    Vbi_3 = (-Emax_eq * W_eq) / 2.0

    Emax_pol = -8e3    # V/cm
    W_pol = 0.5e-4     # cm (0.5 um)
    Vj_3 = (-Emax_pol * W_pol) / 2.0
    Va_3 = Vbi_3 - Vj_3
    print(f"No equilíbrio: E_max = -16 kV/cm e W_0 = 1,0 um -> V_bi = -E_max * W_0 / 2 = {Vbi_3:.2f} V")
    print(f"Polarizado:    E_max = -8 kV/cm  e W   = 0,5 um -> V_j = V_bi - V_a = -E_max * W / 2 = {Vj_3:.2f} V")
    print(f"Tensão de polarização aplicada: V_a = V_bi - V_j = +{Va_3:.2f} V (Polarização Direta!)")

    # -------------------------------------------------------------------------
    # QUESTÃO 4 (Problema 7.6 do Kanaan Kano)
    # -------------------------------------------------------------------------
    print("\n--- QUESTÃO 4 (Lista 2) ---")
    Cj1 = 20.0e-12   # F (para Va1 = -4,3 V)
    Va1 = -4.3       # V
    Cj2 = 40.0e-12   # F (para Va2 = -0,55 V)
    Va2 = -0.55      # V
    A_4 = 2.0e-2     # cm^2
    NA_4 = 1.0e18    # cm^-3

    # Da Aula 13 Slide 1:
    # C_j = A * [ (q * eps_s * N_D * N_A) / (2 * (N_A + N_D) * (V_bi - V_a)) ]^(1/2)
    # Para junção P+N (N_A >> N_D): C_j = A * [ (q * eps_s * N_D) / (2 * (V_bi - V_a)) ]^(1/2)
    # Fazendo a razão (Cj2 / Cj1)^2:
    # (Cj2 / Cj1)^2 = (V_bi - Va1) / (V_bi - Va2)
    razao_quad = (Cj2 / Cj1) ** 2  # (40/20)^2 = 4
    Vbi_4 = (Va2 * razao_quad - Va1) / (razao_quad - 1.0)  # (4.3 - 4*0.55) / 3 = +0.70 V

    # Calculando N_D:
    # C_j^2 = A^2 * q * eps_s * N_D / (2 * (V_bi - V_a))  =>  N_D = 2 * C_j^2 * (V_bi - V_a) / (A^2 * q * eps_s)
    ND_4_117 = (2.0 * (Cj2 ** 2) * (Vbi_4 - Va2)) / ((A_4 ** 2) * q * eps_s_cm)
    eps_s_118 = 11.8 * 8.85e-14
    ND_4_118 = (2.0 * (Cj2 ** 2) * (Vbi_4 - Va2)) / ((A_4 ** 2) * q * eps_s_118)
    print(f"Razão (Cj2 / Cj1)^2 = ({Cj2*1e12:.0f}/{Cj1*1e12:.0f})^2 = {razao_quad:.1f} = (V_bi + 4,3) / (V_bi + 0,55)")
    print(f"b) Built-in voltage: V_bi = {Vbi_4:.2f} V")
    print(f"a) Concentração de doadores N_D (com eps_r = 11,7 da Lista 2): N_D = {ND_4_117:.4e} cm^-3 (~ 6,03 x 10^13 cm^-3)")
    print(f"   Concentração de doadores N_D (com eps_r = 11,8 da Lista 3): N_D = {ND_4_118:.4e} cm^-3 (~ 5,98 x 10^13 cm^-3)")


def resolver_lista_3() -> None:
    banner("LISTA DE EXERCÍCIOS 3 — SCHOTTKY E CAPACITOR MOS (Aula 14 & Kanaan Kano)")

    # Constantes da Lista 3 (página 2) e Aula 14 (Slides 18 e 19)
    k_eV = 8.62e-5          # eV/K
    k_J = 1.38e-23          # J/K
    q = 1.6e-19             # C
    Eg = 1.12               # eV
    eps_0 = 8.85e-12        # F/m
    eps_s = 1.0443e-10      # F/m (11,8 * 8,85e-12 F/m)
    eps_ox_real = 3.4515e-11 # F/m (3,9 * 8,85e-12 F/m — valor físico real / Slide 18: 3,45e-11 F/m)
    eps_ox_typo = 3.4515e-10 # F/m (valor com erro de digitação no expoente na pág. 2 da Lista 3)
    ni = 1.02e10            # cm^-3
    q_chi_s = 4.05          # eV (afinidade eletrônica do silício)
    T = 300.0               # K
    Vt = k_eV * T           # 0,02586 V

    # -------------------------------------------------------------------------
    # QUESTÃO 1 (Lista 3)
    # -------------------------------------------------------------------------
    print("\n--- QUESTÃO 1 (Lista 3) ---")
    ND_1_ini = 1.0e15
    ND_1_fim = 4.8e15
    delta_Vbi = Vt * math.log(ND_1_fim / ND_1_ini)
    print("Pela Aula 14 (Slide 3):")
    print("  1) q*phi_B = q*phi_m - q*chi_s -> Depende APENAS da função trabalho do metal (phi_m) e da")
    print("     afinidade eletrônica do semicondutor (chi_s). NÃO depende da dopagem N_D!")
    print("     Portanto, phi_B FICA CONSTANTE (permanece 0,65 V).")
    print("  2) q*V_bi = q*phi_m - q*phi_s = q*phi_B - (E_C - E_F).")
    print("     Ao aumentar a dopagem de N_D = 10^15 cm^-3 para 4,8 x 10^15 cm^-3, a concentração de elétrons")
    print("     aumenta e o nível de Fermi E_F se aproxima de E_C (a distância E_C - E_F diminui, reduzindo q*phi_s).")
    print(f"     Logo, V_bi AUMENTA! (Especificamente, aumenta em Delta V_bi = (kT/q)*ln(4,8) = +{delta_Vbi:.4f} V,")
    print(f"     passando de 0,40 V para {0.40 + delta_Vbi:.4f} V).")

    # -------------------------------------------------------------------------
    # QUESTÃO 2 (Lista 3)
    # -------------------------------------------------------------------------
    print("\n--- QUESTÃO 2 (Lista 3) ---")
    q_phi_B = 0.65  # eV
    Vbi_2 = 0.40    # V
    print("Pela Aula 14 (Slides 3, 4 e 5):")
    print("  - A barreira do metal para o semicondutor (q*phi_B = q*phi_m - q*chi_s) independe da tensão aplicada!")
    print("  - A barreira do semicondutor para o metal vale q*V_i = q*(V_bi - V_a) = q*(V_bi + V_R).")
    print(f"  a) Polarização direta com V_a = +0,2 V:")
    print(f"     - Barreira semicondutor -> metal: q*(V_bi - V_a) = 0,40 - 0,20 = {Vbi_2 - 0.20:.2f} eV")
    print(f"     - Barreira metal -> semicondutor: q*phi_B = {q_phi_B:.2f} eV (constante)")
    print(f"  b) Polarização reversa com 5 V (V_a = -5 V / V_R = +5 V):")
    print(f"     - Barreira semicondutor -> metal: q*(V_bi - V_a) = 0,40 - (-5,0) = {Vbi_2 + 5.0:.2f} eV")
    print(f"     - Barreira metal -> semicondutor: q*phi_B = {q_phi_B:.2f} eV (constante)")

    # -------------------------------------------------------------------------
    # QUESTÃO 3 (Lista 3)
    # -------------------------------------------------------------------------
    print("\n--- QUESTÃO 3 (Lista 3) ---")
    A_star = 120.0      # A/(cm^2.K^2)
    q_phi_m_Cr = 4.50   # eV (Cromo)
    q_phi_B_3 = q_phi_m_Cr - q_chi_s  # 4,50 - 4,05 = 0,45 eV
    VD_300 = 0.20       # V
    ID_alvo = 0.100     # A (100 mA)
    T1 = 300.0          # K
    T2 = 85.0 + 273.15  # 358,15 K (ou 358 K usando 273)

    # Em T1 = 300 K (Aula 14 Slide 5):
    # I_S = A * A* * T^2 * exp(-q*phi_B / kT)
    # I_D = I_S * [ exp(q*V_D / kT) - 1 ]
    kT_300 = k_eV * T1  # 0,02586 eV
    J_S_300 = A_star * (T1 ** 2) * math.exp(-q_phi_B_3 / kT_300)
    J_D_300 = J_S_300 * (math.exp(VD_300 / kT_300) - 1.0)
    Area_3 = ID_alvo / J_D_300

    # Em T2 = 358 K (85 °C):
    kT_358 = k_eV * 358.0
    IS_358 = Area_3 * A_star * (358.0 ** 2) * math.exp(-q_phi_B_3 / kT_358)
    VD_358 = kT_358 * math.log(1.0 + (ID_alvo / IS_358))

    print(f"Barreira Schottky Cr/Si: q*phi_B = q*phi_m - q*chi_s = 4,50 - 4,05 = {q_phi_B_3:.2f} eV")
    print(f"Em T = 300 K (kT = {kT_300:.5f} eV):")
    print(f"  Densidade de corrente de saturação: J_S(300K) = {J_S_300:.4e} A/cm^2")
    print(f"  Área do diodo: A = {Area_3:.4e} cm^2 ({Area_3 * 100:.4f} mm^2)")
    print(f"Em T = 85 °C (358 K, kT = {kT_358:.5f} eV):")
    print(f"  Nova corrente de saturação: I_S(358K) = {IS_358:.4e} A ({IS_358 * 1e3:.4f} mA)")
    print(f"  Potencial necessário para I_D = 100 mA: V_D = {VD_358:.4f} V (~ 0,141 V)")

    # -------------------------------------------------------------------------
    # QUESTÃO 4 (Lista 3)
    # -------------------------------------------------------------------------
    print("\n--- QUESTÃO 4 (Lista 3) ---")
    V_FB_4 = -1.0     # V
    t_ox_4 = 5.0e-9   # m (5 nm = 5 x 10^-7 cm)
    V_G_4 = 0.0       # V
    # Substrato Tipo N com V_FB = -1 V e V_G = 0 V:
    # Pela tabela da Lista 3 (pág. 2): Para Tipo N, quando V_G > V_FB (0 V > -1 V), o capacitor está em ACUMULAÇÃO!
    # Em Acumulação, o potencial de superfície phi_s é desprezível (phi_s ~ 0).
    # Assim, toda a diferença de tensão V_ox = V_G - V_FB = 0 - (-1 V) = +1 V cai sobre o óxido!
    V_ox_4 = V_G_4 - V_FB_4  # +1,0 V
    E_ox_m = abs(V_ox_4) / t_ox_4
    E_ox_cm = E_ox_m * 1e-2
    print(f"Como o substrato é Tipo N e V_G = 0 V > V_FB = -1 V, a estrutura está em ACUMULAÇÃO (tabela da Lista 3).")
    print(f"Em acumulação, phi_s é desprezível (phi_s ~ 0), logo V_ox = V_G - V_FB = 0 - (-1) = +1,0 V.")
    print(f"Módulo do campo elétrico no óxido: E_ox = |V_G - V_FB| / t_ox = 1 V / 5 nm = {E_ox_m:.2e} V/m = {E_ox_cm:.2e} V/cm (2 MV/cm).")
    print("Sentido do campo elétrico: Como V_G > V_FB, acumulam-se elétrons (carga negativa) na superfície do")
    print("semicondutor Tipo N e cargas positivas no eletrodo de porta (metal). O campo elétrico aponta das cargas")
    print("positivas para as negativas, portanto no sentido: ÓXIDO -> SEMICONDUTOR (da porta para o substrato)!")

    # -------------------------------------------------------------------------
    # QUESTÃO 5 (Lista 3)
    # -------------------------------------------------------------------------
    print("\n--- QUESTÃO 5 (Lista 3) ---")
    # a) Silício fortemente dopado com boro = P+-Si (boro é aceitador, grupo III).
    #    Pela tabela da Aula 14 (Slide 19): Função trabalho do P+-Si é q*phi_m = 5,17 eV (pois E_F ~ E_V, logo q*chi_s + E_g = 4,05 + 1,12 = 5,17 eV).
    # b) Substrato de silício tipo P com N_A = 10^16 cm^-3:
    #    Pela Aula 14 (Slide 11): q*phi_s = q*chi_s + E_g/2 + q*phi_F, onde phi_F = (kT/q) * ln(N_A / n_i).
    NA_5 = 1.0e16
    q_phi_m_5 = 5.17  # eV (P+-Si, Aula 14 Slide 19)
    q_phi_F_5 = Vt * math.log(NA_5 / ni)
    q_phi_s_5 = q_chi_s + (Eg / 2.0) + q_phi_F_5
    q_phi_ms_5 = q_phi_m_5 - q_phi_s_5
    print(f"Eletrodo de porta (Si fortemente dopado com boro = P+-Si, Slide 19 Aula 14): q*phi_m = {q_phi_m_5:.2f} eV")
    print(f"Potencial de Fermi do substrato P (N_A = 10^16 cm^-3): q*phi_F = kT*ln(N_A/n_i) = {q_phi_F_5:.4f} eV")
    print(f"Função trabalho do substrato P: q*phi_s = q*chi_s + E_g/2 + q*phi_F = 4,05 + 0,56 + {q_phi_F_5:.4f} = {q_phi_s_5:.4f} eV")
    print(f"Diferença de função trabalho: q*phi_ms = q*phi_m - q*phi_s = {q_phi_m_5:.2f} - {q_phi_s_5:.4f} = +{q_phi_ms_5:.4f} eV (~ +0,203 eV)")

    # -------------------------------------------------------------------------
    # QUESTÃO 6 (Lista 3)
    # -------------------------------------------------------------------------
    print("\n--- QUESTÃO 6 (Lista 3) ---")
    VT_6 = 0.25       # V
    VG_6 = 5.0        # V
    t_ox_6 = 15.0e-9  # m (15 nm)
    # Substrato Tipo P com V_G = 5 V > V_T = 0,25 V -> INVERSÃO FORTE!
    # Tipo dos portadores móveis na camada de inversão do substrato Tipo P: ELÉTRONS!
    # Pela tabela da Lista 3 (pág. 2): |Q_I| = |V_G - V_T| * C_ox, onde C_ox = eps_ox / t_ox.
    # Densidade superficial de portadores (elétrons/área): n_s = |Q_I| / q.
    Cox_6_real = eps_ox_real / t_ox_6
    QI_6_real = abs(VG_6 - VT_6) * Cox_6_real
    ns_6_real_m2 = QI_6_real / q
    ns_6_real_cm2 = ns_6_real_m2 * 1e-4

    Cox_6_typo = eps_ox_typo / t_ox_6
    QI_6_typo = abs(VG_6 - VT_6) * Cox_6_typo
    ns_6_typo_m2 = QI_6_typo / q
    ns_6_typo_cm2 = ns_6_typo_m2 * 1e-4

    print("1) Tipo de portadores na superfície: Como o substrato é Tipo P e V_G = 5 V > V_T = 0,25 V,")
    print("   o capacitor opera em INVERSÃO FORTE. Logo, os portadores na superfície são ELÉTRONS!")
    print("2) Densidade superficial de portadores (usando eps_ox = 3,4515 x 10^-11 F/m real / Slide 18):")
    print(f"   C_ox = eps_ox / t_ox = {Cox_6_real:.4e} F/m^2")
    print(f"   |Q_I| = |V_G - V_T| * C_ox = {QI_6_real:.4e} C/m^2 ({QI_6_real * 1e-4:.4e} C/cm^2)")
    print(f"   n_s = |Q_I| / q = {ns_6_real_m2:.4e} elétrons/m^2 = {ns_6_real_cm2:.4e} elétrons/cm^2")
    print("   [Nota: Caso se utilize literalmente o valor impresso com typo na folha da Lista 3, eps_ox = 3,4515 x 10^-10 F/m:")
    print(f"    |Q_I| = {QI_6_typo:.4e} C/m^2 e n_s = {ns_6_typo_m2:.4e} m^-2 = {ns_6_typo_cm2:.4e} cm^-2]")

    # -------------------------------------------------------------------------
    # QUESTÃO 7 (Lista 3)
    # -------------------------------------------------------------------------
    print("\n--- QUESTÃO 7 (Lista 3) ---")
    C_acc = 9.0e-3  # F/m^2 (9 mF/m^2 em VG = -2 V)
    C_inv = 3.0e-3  # F/m^2 (3 mF/m^2 em VG = +2 V, HF)
    t_ox_7_real = eps_ox_real / C_acc
    t_ox_7_typo = eps_ox_typo / C_acc
    w_d_inv = eps_s * ((1.0 / C_inv) - (1.0 / C_acc))
    print("1) Tipo de dopagem do substrato:")
    print("   A acumulação ocorre em V_G = -2 V (negativo) e a inversão forte em V_G = +2 V (positivo).")
    print("   Pela tabela da Lista 3 (Acumulação para V_G < V_FB e Inversão Forte para V_G > V_T),")
    print("   como um potencial negativo na porta atrai lacunas para acumular na superfície, o substrato é TIPO P!")
    print("2) Espessura do óxido de porta (t_ox):")
    print("   Em acumulação, C = C_ox = eps_ox / t_ox => t_ox = eps_ox / C_ox:")
    print(f"   - Usando eps_ox = 3,4515 x 10^-11 F/m (valor físico real 3,9*eps_0 / Slide 18): t_ox = {t_ox_7_real:.4e} m = {t_ox_7_real * 1e9:.3f} nm")
    print(f"   - Usando eps_ox = 3,4515 x 10^-10 F/m (literal impresso na Lista 3):            t_ox = {t_ox_7_typo:.4e} m = {t_ox_7_typo * 1e9:.2f} nm")
    print(f"   - Bônus (largura de depleção máxima na inversão forte HF): w_d-inv = {w_d_inv * 1e9:.2f} nm")


if __name__ == "__main__":
    resolver_lista_2()
    resolver_lista_3()
