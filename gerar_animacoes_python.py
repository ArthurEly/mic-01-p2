#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MIC 01 - Física de Dispositivos Semicondutores
Gerador de Animações Didáticas em Python (Matplotlib + NumPy + Pillow)
Gera 5 animações em formato GIF cobrindo todos os conceitos e questões das Listas 2 e 3.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "animacoes")
os.makedirs(OUT_DIR, exist_ok=True)

# Estilo visual escuro e didático
plt.rcParams.update({
    "figure.facecolor": "#0f172a",
    "axes.facecolor": "#1e293b",
    "axes.edgecolor": "#475569",
    "axes.labelcolor": "#e2e8f0",
    "text.color": "#f8fafc",
    "xtick.color": "#cbd5e1",
    "ytick.color": "#cbd5e1",
    "grid.color": "#334155",
    "grid.linestyle": "--",
    "grid.alpha": 0.5,
    "font.size": 10,
})


def anim_1_juncao_pn_eletrostatica():
    """
    Animação 1: Eletrostática da Junção P+N (Densidade de Carga, Campo Elétrico, Potencial e Bandas)
    Ilustra as Aulas 8, 9 e 10 e a Questão 3 da Lista 2 (V_bi = 0,8 V, E_max = -16 kV/cm -> -8 kV/cm em Va = +0,6 V).
    """
    print("Gerando anim_1_juncao_pn_eletrostatica.gif ...")
    fig, axes = plt.subplots(2, 2, figsize=(12, 7.5), dpi=100)
    fig.subplots_adjust(hspace=0.38, wspace=0.28, top=0.88, bottom=0.09)

    ax_rho, ax_E = axes[0, 0], axes[0, 1]
    ax_V, ax_band = axes[1, 0], axes[1, 1]

    # Parâmetros inspirados na Questão 3 da Lista 2:
    # No equilíbrio (Va = 0 V): Vbi = 0,80 V, W0 = 1,0 um (lado N domina: xn0 = 1,0 um, xp0 = 0,15 um para visualização)
    Vbi = 0.80
    # Varredura de Va de -1.0 V (reversa) até +0.60 V (direta - Questão 3 Lista 2)
    va_vals = np.concatenate([
        np.linspace(-1.0, 0.0, 18),
        np.zeros(5),
        np.linspace(0.0, 0.60, 18),
        np.full(7, 0.60),
    ])

    x = np.linspace(-0.6, 1.8, 500)  # em um

    def update(frame):
        Va = va_vals[frame]
        Vj = max(Vbi - Va, 0.05)
        scale = np.sqrt(Vj / Vbi)

        xn = 1.0 * scale       # um (em Va=0: 1.0 um; em Va=0.6V: 0.5 um)
        xp = 0.12 * scale      # um (lado P+ muito mais dopado)
        Emax = -16.0 * scale   # kV/cm (em Va=0: -16 kV/cm; em Va=0.6V: -8 kV/cm)

        for ax in (ax_rho, ax_E, ax_V, ax_band):
            ax.clear()
            ax.grid(True)

        regime = "EQUILÍBRIO TÉRMICO (Va = 0 V)"
        cor_regime = "#38bdf8"
        if Va < -0.01:
            regime = f"POLARIZAÇÃO REVERSA (Va = {Va:+.2f} V) — Depleção Alarga"
            cor_regime = "#f43f5e"
        elif Va > 0.01:
            regime = f"POLARIZAÇÃO DIRETA (Va = {Va:+.2f} V) — Barreira Reduz"
            if abs(Va - 0.60) < 0.02:
                regime += " [Ponto da Questão 3 - Lista 2!]"
            cor_regime = "#10b981"

        fig.suptitle(
            f"Junção P⁺N: Carga, Campo Elétrico, Potencial e Bandas (Aulas 8–10 | Lista 2 Q1, Q2d, Q3)\n{regime}",
            fontsize=12, fontweight="bold", color=cor_regime
        )

        # 1) Densidade de carga rho(x)
        rho = np.zeros_like(x)
        rho[(x >= -xp) & (x < 0)] = -8.0
        rho[(x >= 0) & (x <= xn)] = +1.0
        ax_rho.plot(x, rho, color="#facc15", lw=2.2)
        ax_rho.fill_between(x, 0, rho, where=(rho < 0), color="#3b82f6", alpha=0.45, label="Aceitadores $-qN_A$ (P⁺)")
        ax_rho.fill_between(x, 0, rho, where=(rho > 0), color="#ef4444", alpha=0.45, label="Doadores $+qN_D$ (N)")
        ax_rho.axvline(0, color="#94a3b8", ls=":", lw=1)
        ax_rho.set_xlim(-0.5, 1.7)
        ax_rho.set_ylim(-9.5, 3.0)
        ax_rho.set_title(f"1. Densidade Espacial de Carga $\\rho(x)$ ($W \\approx {xn:.2f}\\ \\mu$m)", fontsize=10.5)
        ax_rho.set_xlabel("Posição $x$ ($\\mu$m)")
        ax_rho.set_ylabel("$\\rho(x)$ (unid. arb.)")
        ax_rho.legend(loc="lower right", fontsize=8, facecolor="#0f172a")

        # 2) Campo Elétrico E(x) — Destaque para a Questão 3 da Lista 2
        E = np.zeros_like(x)
        mask_p = (x >= -xp) & (x < 0)
        mask_n = (x >= 0) & (x <= xn)
        E[mask_p] = Emax * (1.0 + x[mask_p] / xp)
        E[mask_n] = Emax * (1.0 - x[mask_n] / xn)

        ax_E.plot(x, E, color="#f43f5e", lw=2.5)
        ax_E.fill_between(x, 0, E, color="#f43f5e", alpha=0.30,
                          label=f"Área = $-(V_{{bi}}-V_a) = -{Vj:.2f}$ V")
        ax_E.axvline(0, color="#94a3b8", ls=":", lw=1)
        ax_E.scatter([0], [Emax], color="#facc15", zorder=5, s=45)
        ax_E.annotate(f"$\\mathcal{{E}}_{{max}} = {Emax:.1f}$ kV/cm",
                      xy=(0, Emax), xytext=(0.25, Emax - 2.0),
                      color="#facc15", fontweight="bold", fontsize=9,
                      arrowprops=dict(arrowstyle="->", color="#facc15"))
        ax_E.set_xlim(-0.5, 1.7)
        ax_E.set_ylim(-25.0, 2.0)
        ax_E.set_title("2. Perfil de Campo Elétrico $\\mathcal{E}(x)$ (Lista 2 - Q3)", fontsize=10.5)
        ax_E.set_xlabel("Posição $x$ ($\\mu$m)")
        ax_E.set_ylabel("$\\mathcal{E}(x)$ (kV/cm)")
        ax_E.legend(loc="lower right", fontsize=8.5, facecolor="#0f172a")

        # 3) Potencial Eletrostático V(x)
        V = np.zeros_like(x)
        Vp_max = Vj * (xp / (xp + xn))
        V[mask_p] = Vp_max * ((x[mask_p] + xp) / xp) ** 2
        V[mask_n] = Vp_max + (Vj - Vp_max) * (1.0 - ((xn - x[mask_n]) / xn) ** 2)
        V[x > xn] = Vj

        ax_V.plot(x, V, color="#38bdf8", lw=2.5, label=f"$V(x)$ com polarização $V_a={Va:+.2f}$ V")
        # Curva de equilíbrio pontilhada para comparação (Aula 10 Slide 3)
        xn0, xp0 = 1.0, 0.12
        V0 = np.zeros_like(x)
        Vp0 = Vbi * (xp0 / (xp0 + xn0))
        m_p0 = (x >= -xp0) & (x < 0)
        m_n0 = (x >= 0) & (x <= xn0)
        V0[m_p0] = Vp0 * ((x[m_p0] + xp0) / xp0) ** 2
        V0[m_n0] = Vp0 + (Vbi - Vp0) * (1.0 - ((xn0 - x[m_n0]) / xn0) ** 2)
        V0[x > xn0] = Vbi
        ax_V.plot(x, V0, color="#94a3b8", ls="--", lw=1.5, label=f"Equilíbrio ($V_{{bi}} = {Vbi:.2f}$ V)")

        ax_V.set_xlim(-0.5, 1.7)
        ax_V.set_ylim(-0.1, 2.0)
        ax_V.set_title(f"3. Potencial Eletrostático $\\phi(x)$: Barreira $V_j = V_{{bi}} - V_a = {Vj:.2f}$ V", fontsize=10.5)
        ax_V.set_xlabel("Posição $x$ ($\\mu$m)")
        ax_V.set_ylabel("Potencial $\\phi(x)$ (V)")
        ax_V.legend(loc="upper left", fontsize=8, facecolor="#0f172a")

        # 4) Diagrama de Bandas de Energia (E = -q*phi)
        Eg = 1.12
        Ec = 1.2 - V
        Ev = Ec - Eg
        Ei = Ec - Eg / 2.0
        ax_band.plot(x, Ec, color="#60a5fa", lw=2.4, label="$E_C$ (Banda de Condução)")
        ax_band.plot(x, Ei, color="#94a3b8", ls=":", lw=1.4, label="$E_i$ (Intríns.)")
        ax_band.plot(x, Ev, color="#f472b6", lw=2.4, label="$E_V$ (Banda de Valência)")
        # Quasi-Fermi levels
        EFp = Ec[0] - Eg + 0.08
        EFn = EFp - Va
        ax_band.hlines(EFp, -0.5, 0.0, color="#facc15", ls="--", lw=1.8, label="$E_{Fp}, E_{Fn}$")
        ax_band.hlines(EFn, 0.0, 1.7, color="#facc15", ls="--", lw=1.8)
        ax_band.set_xlim(-0.5, 1.7)
        ax_band.set_ylim(-1.9, 1.5)
        ax_band.set_title(f"4. Diagrama de Bandas: Barreira $q(V_{{bi}}-V_a) = {Vj:.2f}$ eV", fontsize=10.5)
        ax_band.set_xlabel("Posição $x$ ($\\mu$m)")
        ax_band.set_ylabel("Energia dos Elétrons $E$ (eV)")
        ax_band.legend(loc="lower left", fontsize=7.5, facecolor="#0f172a")

    anim = FuncAnimation(fig, update, frames=len(va_vals), interval=120)
    out_path = os.path.join(OUT_DIR, "anim_1_juncao_pn_eletrostatica.gif")
    anim.save(out_path, writer=PillowWriter(fps=8))
    plt.close(fig)
    print(f"Salvo: {out_path}")


def anim_2_injecao_correntes_pn():
    """
    Animação 2: Injeção de Portadores Minoritários e Corrente no Diodo n+p (Aulas 11 e 12 | Lista 2 Q2).
    """
    print("Gerando anim_2_injecao_correntes_pn.gif ...")
    fig, (ax_prof, ax_iv) = plt.subplots(1, 2, figsize=(12, 5.2), dpi=100)
    fig.subplots_adjust(wspace=0.28, top=0.83, bottom=0.14)

    # Dados da Questão 2 da Lista 2:
    # Diodo n+p: ND = 1e18, NA = 1e16, Lp = 36.06 um, Ln = 58.31 um, Is = 1.1265e-15 A
    Lp = 36.06   # um
    Ln = 58.31   # um
    Is = 1.1265e-15  # A
    Vt = 0.02586     # V

    va_vals = np.concatenate([
        np.linspace(-0.5, 0.0, 12),
        np.linspace(0.0, 0.50, 22),
        np.full(8, 0.50),
    ])

    x_p = np.linspace(-180, -5, 200)  # região P (um)
    x_n = np.linspace(5, 180, 200)    # região N+ (um)
    v_curve = np.linspace(-0.55, 0.55, 300)
    i_curve = Is * (np.exp(v_curve / Vt) - 1.0) * 1e9  # em nA

    def update(frame):
        Va = va_vals[frame]
        ax_prof.clear()
        ax_iv.clear()
        ax_prof.grid(True)
        ax_iv.grid(True)

        # Excesso normalizado (para visualização didática das curvas exponenciais da Aula 11 Slide 5)
        fator = np.tanh(Va / 0.15)  # escala suave visual para mostrar tanto Va<0 (extração) quanto Va>0 (injeção)
        n_norm = 1.0 + 0.85 * fator * np.exp((x_p + 5.0) / Ln)
        p_norm = 0.35 + 0.28 * fator * np.exp(-(x_n - 5.0) / Lp)

        ax_prof.axvspan(-5, 5, color="#475569", alpha=0.45, label="Zona de Depleção $W$")
        ax_prof.axhline(1.0, xmin=0, xmax=0.47, color="#60a5fa", ls=":", lw=1.2)
        ax_prof.axhline(0.35, xmin=0.53, xmax=1.0, color="#f472b6", ls=":", lw=1.2)
        ax_prof.plot(x_p, n_norm, color="#38bdf8", lw=2.6, label=f"Elétrons minoritários no lado P ($L_n={Ln:.1f}\\ \\mu$m)")
        ax_prof.plot(x_n, p_norm, color="#f43f5e", lw=2.6, label=f"Lacunas minoritárias no lado N⁺ ($L_p={Lp:.1f}\\ \\mu$m)")

        ax_prof.set_xlim(-180, 180)
        ax_prof.set_ylim(0.0, 2.1)
        ax_prof.set_title(f"1. Perfil de Portadores Minoritários (Aula 11 | $V_a = {Va:+.2f}$ V)", fontsize=10.5)
        ax_prof.set_xlabel("Distância à Junção $x$ ($\\mu$m)")
        ax_prof.set_ylabel("Concentração Relativa (escala didática)")
        ax_prof.legend(loc="upper right", fontsize=8, facecolor="#0f172a")

        # Curva I-V (Questão 2 da Lista 2)
        I_atual = Is * (np.exp(Va / Vt) - 1.0)
        ax_iv.plot(v_curve, i_curve, color="#10b981", lw=2.4, label="$I(V_a) = I_S(e^{qV_a/kT} - 1)$")
        ax_iv.scatter([Va], [I_atual * 1e9], color="#facc15", s=65, zorder=5)

        if Va >= 0.45:
            txt_i = f"$V_a = +0,50$ V (Lista 2 Q2b)\n$I = {I_atual*1e6:.3f}\\ \\mu$A ($2,81\\times 10^{{-7}}$ A)"
        elif Va <= -0.45:
            txt_i = f"$V_a = -0,50$ V (Lista 2 Q2c)\n$I \\approx -I_S = -1,13\\times 10^{{-15}}$ A"
        else:
            txt_i = f"$V_a = {Va:+.2f}$ V\n$I = {I_atual:.2e}$ A"

        ax_iv.annotate(txt_i, xy=(Va, I_atual * 1e9), xytext=(-0.45, 180),
                       color="#facc15", fontweight="bold", fontsize=9.5,
                       bbox=dict(boxstyle="round,pad=0.4", facecolor="#0f172a", edgecolor="#facc15"),
                       arrowprops=dict(arrowstyle="->", color="#facc15"))

        ax_iv.set_xlim(-0.55, 0.55)
        ax_iv.set_ylim(-25, 310)
        ax_iv.set_title("2. Característica I–V do Diodo $n^+p$ (Lista 2 - Q2: $I_S = 1,13$ fA)", fontsize=10.5)
        ax_iv.set_xlabel("Tensão Aplicada $V_a$ (V)")
        ax_iv.set_ylabel("Corrente $I$ (nA)")
        ax_iv.legend(loc="upper left", fontsize=8.5, facecolor="#0f172a")

        fig.suptitle(
            "Diodo de Silício $n^+p$ (Aulas 11–12 | Lista 2 - Questão 2): Difusão de Minoritários e Equação de Shockley",
            fontsize=12, fontweight="bold", color="#38bdf8"
        )

    anim = FuncAnimation(fig, update, frames=len(va_vals), interval=120)
    out_path = os.path.join(OUT_DIR, "anim_2_injecao_correntes_pn.gif")
    anim.save(out_path, writer=PillowWriter(fps=8))
    plt.close(fig)
    print(f"Salvo: {out_path}")


def anim_3_capacitancia_deplecao():
    """
    Animação 3: Capacitância da Junção P+N em Polarização Reversa e Extração de V_bi e N_D (Aula 13 | Lista 2 Q4).
    """
    print("Gerando anim_3_capacitancia_deplecao.gif ...")
    fig, (ax_c, ax_inv) = plt.subplots(1, 2, figsize=(12, 5.2), dpi=100)
    fig.subplots_adjust(wspace=0.28, top=0.83, bottom=0.14)

    # Dados exatos da Questão 4 da Lista 2:
    # Va1 = -4,3 V -> Cj1 = 20 pF | Va2 = -0,55 V -> Cj2 = 40 pF
    # Vbi = 0,70 V, ND = 6,03e13 cm^-3, A = 2e-2 cm^2
    Vbi = 0.70
    k_const = 40.0 * np.sqrt(0.70 - (-0.55))  # Cj(pF) * sqrt(Vbi - Va) = 40 * sqrt(1.25) = 44.72136 pF*V^0.5
    va_grid = np.linspace(-5.0, 0.4, 300)
    cj_grid = k_const / np.sqrt(Vbi - va_grid)

    va_line = np.linspace(-5.0, Vbi, 300)
    inv_c2_line = (Vbi - va_line) / (k_const ** 2) * 1e4  # em 10^-4 pF^-2

    va_anim = np.concatenate([
        np.linspace(-0.55, -4.30, 20),
        np.full(6, -4.30),
        np.linspace(-4.30, -0.55, 20),
        np.full(6, -0.55),
    ])

    def update(frame):
        Va = va_anim[frame]
        Cj = k_const / np.sqrt(Vbi - Va)
        inv_c2 = ((Vbi - Va) / (k_const ** 2)) * 1e4

        ax_c.clear()
        ax_inv.clear()
        ax_c.grid(True)
        ax_inv.grid(True)

        # Painel 1: Cj vs Va
        ax_c.plot(va_grid, cj_grid, color="#38bdf8", lw=2.5, label="$C_j(V_a) = A\\sqrt{\\frac{q\\varepsilon_s N_D}{2(V_{bi}-V_a)}}$")
        ax_c.scatter([-4.3, -0.55], [20.0, 40.0], color="#10b981", s=70, zorder=5, label="Pontos da Questão 4 (Lista 2)")
        ax_c.scatter([Va], [Cj], color="#facc15", s=80, zorder=6)
        ax_c.annotate("(-4,3 V; 20 pF)", xy=(-4.3, 20), xytext=(-4.7, 29),
                      color="#10b981", fontweight="bold", arrowprops=dict(arrowstyle="->", color="#10b981"))
        ax_c.annotate("(-0,55 V; 40 pF)", xy=(-0.55, 40), xytext=(-2.6, 48),
                      color="#10b981", fontweight="bold", arrowprops=dict(arrowstyle="->", color="#10b981"))
        ax_c.set_xlim(-5.0, 0.6)
        ax_c.set_ylim(10, 85)
        ax_c.set_title(f"1. Capacitância de Depleção $C_j$: Em $V_a={Va:.2f}$ V $\\rightarrow C_j={Cj:.1f}$ pF", fontsize=10.5)
        ax_c.set_xlabel("Tensão Aplicada $V_a$ (V)")
        ax_c.set_ylabel("Capacitância $C_j$ (pF)")
        ax_c.legend(loc="upper left", fontsize=8.5, facecolor="#0f172a")

        # Painel 2: 1/Cj^2 vs Va (Linearização para extrair Vbi e ND!)
        ax_inv.plot(va_line, inv_c2_line, color="#f472b6", lw=2.5, label="Reta $1/C_j^2 = \\frac{2(V_{bi}-V_a)}{q\\varepsilon_s A^2 N_D}$")
        ax_inv.scatter([-4.3, -0.55], [1e4 / 400.0, 1e4 / 1600.0], color="#10b981", s=70, zorder=5)
        ax_inv.scatter([Vbi], [0.0], color="#facc15", s=80, zorder=6, label=f"Intercepto: $V_{{bi}} = +{Vbi:.2f}$ V")
        ax_inv.scatter([Va], [inv_c2], color="#facc15", s=80, zorder=6)
        ax_inv.axvline(0, color="#94a3b8", ls=":", lw=1)
        ax_inv.annotate(f"Intercepto $1/C_j^2 = 0$:\n$V_{{bi}} = +0,70$ V\nInclinação $\\rightarrow N_D = 6,03\\times 10^{{13}}$ cm$^{{-3}}$",
                        xy=(Vbi, 0.0), xytext=(-3.2, 16.5),
                        color="#facc15", fontweight="bold", fontsize=9,
                        bbox=dict(boxstyle="round,pad=0.4", facecolor="#0f172a", edgecolor="#facc15"),
                        arrowprops=dict(arrowstyle="->", color="#facc15"))
        ax_inv.set_xlim(-5.0, 1.2)
        ax_inv.set_ylim(-1.5, 28.0)
        ax_inv.set_title("2. Gráfico Linearizado $1/C_j^2 \\times V_a$ (Extração de $V_{bi}$ e $N_D$)", fontsize=10.5)
        ax_inv.set_xlabel("Tensão Aplicada $V_a$ (V)")
        ax_inv.set_ylabel("$1/C_j^2$ ($10^{-4}$ pF$^{-2}$)")
        ax_inv.legend(loc="upper right", fontsize=8.5, facecolor="#0f172a")

        fig.suptitle(
            "Capacitância de Junção $P^+N$ (Aula 13 | Lista 2 - Questão 4): $V_{bi} = 0,70$ V e $N_D = 6,03\\times 10^{13}$ cm$^{-3}$",
            fontsize=12, fontweight="bold", color="#f472b6"
        )

    anim = FuncAnimation(fig, update, frames=len(va_anim), interval=120)
    out_path = os.path.join(OUT_DIR, "anim_3_capacitancia_deplecao.gif")
    anim.save(out_path, writer=PillowWriter(fps=8))
    plt.close(fig)
    print(f"Salvo: {out_path}")


def anim_4_diodo_schottky():
    """
    Animação 4: Diodo Schottky Metal-Semicondutor (Aula 14 Slides 2–5 | Lista 3 Q1, Q2, Q3).
    Mostra o diagrama de bandas (q*phi_B constante vs q*(V_bi - V_a) variável) e o efeito da temperatura (Q3).
    """
    print("Gerando anim_4_diodo_schottky.gif ...")
    fig, (ax_band, ax_iv) = plt.subplots(1, 2, figsize=(12, 5.4), dpi=100)
    fig.subplots_adjust(wspace=0.28, top=0.83, bottom=0.14)

    # Lista 3 Q1 e Q2: q*phi_B = 0,65 eV, Vbi = 0,40 V (ou 0,44 V com ND=4,8e15)
    # Lista 3 Q3: Cr/Si -> q*phi_B = 0,45 eV, A = 1,463e-4 cm^2, ID = 100 mA em VD=0,20V (300K) e VD=0,141V (85°C)
    va_vals = np.concatenate([
        np.linspace(-1.0, 0.0, 15),
        np.zeros(5),
        np.linspace(0.0, 0.25, 15),
        np.full(5, 0.20),
    ])

    x_semi = np.linspace(0.0, 1.5, 200)
    vd_grid = np.linspace(0.0, 0.24, 250)
    Area_q3 = 1.4631e-4
    A_star = 120.0
    k_eV = 8.62e-5
    phi_B_Cr = 0.45

    IS_300 = Area_q3 * A_star * (300.0 ** 2) * np.exp(-phi_B_Cr / (k_eV * 300.0))
    IS_358 = Area_q3 * A_star * (358.0 ** 2) * np.exp(-phi_B_Cr / (k_eV * 358.0))
    I_300 = IS_300 * (np.exp(vd_grid / (k_eV * 300.0)) - 1.0) * 1e3  # mA
    I_358 = IS_358 * (np.exp(vd_grid / (k_eV * 358.0)) - 1.0) * 1e3  # mA

    def update(frame):
        Va = va_vals[frame]
        ax_band.clear()
        ax_iv.clear()
        ax_band.grid(True)
        ax_iv.grid(True)

        # Painel 1: Diagrama de Bandas Schottky (Lista 3 Q1 & Q2: phi_B = 0.65 eV, Vbi = 0.40 V)
        phi_B = 0.65
        Vbi = 0.40
        Ec_FB = phi_B - Vbi  # 0.25 eV acima de EF_semi no volume
        Vj = max(Vbi - Va, 0.05)
        W = 0.8 * np.sqrt(Vj / Vbi)

        # Metal em x < 0: EF_m = 0 eV (referência)
        ax_band.axvspan(-0.6, 0.0, color="#f59e0b", alpha=0.25, label="Metal ($E_{Fm} = 0$ eV)")
        ax_band.hlines(0.0, -0.6, 0.0, color="#facc15", lw=2.8)

        # Semicondutor Tipo N em x >= 0:
        # EF_s desloca de -q*Va em relação ao metal: EF_s = +Va
        EF_s = Va
        Ec_bulk = EF_s + Ec_FB
        Ec = np.full_like(x_semi, Ec_bulk)
        mask_w = x_semi <= W
        # Na interface x=0, Ec(0) = EF_m + q*phi_B = +0,65 eV SEMPRE!
        Ec[mask_w] = Ec_bulk + Vj * ((W - x_semi[mask_w]) / W) ** 2
        Ev = Ec - 1.12

        ax_band.plot(x_semi, Ec, color="#38bdf8", lw=2.6, label="$E_C$ (Semicondutor Tipo N)")
        ax_band.plot(x_semi, Ev, color="#f472b6", lw=2.2, label="$E_V$")
        ax_band.hlines(EF_s, 0.0, 1.5, color="#10b981", ls="--", lw=2.0, label=f"$E_{{Fs}}$ ($V_a = {Va:+.2f}$ V)")

        # Seta de q*phi_B (SEMPRE 0.65 eV!) e q*(Vbi - Va)
        ax_band.annotate("", xy=(-0.08, phi_B), xytext=(-0.08, 0.0),
                         arrowprops=dict(arrowstyle="<->", color="#facc15", lw=2.2))
        ax_band.text(-0.55, phi_B / 2.0, f"$q\\varphi_B = {phi_B:.2f}$ eV\n(FIXO!)", color="#facc15", fontweight="bold", fontsize=9)

        ax_band.annotate("", xy=(W + 0.05, phi_B), xytext=(W + 0.05, Ec_bulk),
                         arrowprops=dict(arrowstyle="<->", color="#38bdf8", lw=2.2))
        ax_band.text(W + 0.10, (phi_B + Ec_bulk) / 2.0,
                     f"$q(V_{{bi}}-V_a)$\n$= {Vj:.2f}$ eV", color="#38bdf8", fontweight="bold", fontsize=9)

        ax_band.set_xlim(-0.6, 1.5)
        ax_band.set_ylim(-0.9, 1.1)
        ax_band.set_title("1. Bandas do Diodo Schottky (Lista 3 - Q1 e Q2)", fontsize=10.5)
        ax_band.set_xlabel("Posição $x$ (Metal $\\leftarrow 0 \\rightarrow$ Semicondutor N)")
        ax_band.set_ylabel("Energia $E$ (eV)")
        ax_band.legend(loc="lower right", fontsize=8, facecolor="#0f172a")

        # Painel 2: Curvas I-V em 300 K e 85 °C (358 K) para Lista 3 Q3
        ax_iv.plot(vd_grid, I_300, color="#38bdf8", lw=2.5, label="$T = 300$ K ($V_D = 0,200$ V $\\rightarrow 100$ mA)")
        ax_iv.plot(vd_grid, I_358, color="#f43f5e", lw=2.5, label="$T = 85\\ ^\\circ$C ($358$ K: $V_D = 0,141$ V $\\rightarrow 100$ mA)")
        ax_iv.axhline(100.0, color="#facc15", ls=":", lw=1.8, label="Corrente Alvo $I_D = 100$ mA")
        ax_iv.scatter([0.20, 0.1411], [100.0, 100.0], color="#facc15", s=75, zorder=5)
        ax_iv.annotate("$V_D(85^\\circ\\mathrm{C}) = 0,141$ V", xy=(0.1411, 100.0), xytext=(0.02, 130.0),
                       color="#facc15", fontweight="bold", arrowprops=dict(arrowstyle="->", color="#facc15"))
        ax_iv.annotate("$V_D(300\\ \\mathrm{K}) = 0,200$ V\n$A = 1,46\\times 10^{-4}$ cm$^2$", xy=(0.20, 100.0), xytext=(0.13, 35.0),
                       color="#38bdf8", fontweight="bold", arrowprops=dict(arrowstyle="->", color="#38bdf8"))

        ax_iv.set_xlim(0.0, 0.23)
        ax_iv.set_ylim(0.0, 180.0)
        ax_iv.set_title("2. Emissão Termiônica Cr/Si: Efeito de $T$ (Lista 3 - Q3)", fontsize=10.5)
        ax_iv.set_xlabel("Tensão Direta Aplicada $V_D$ (V)")
        ax_iv.set_ylabel("Corrente $I_D$ (mA)")
        ax_iv.legend(loc="upper left", fontsize=8, facecolor="#0f172a")

        fig.suptitle(
            "Junção Metal-Semicondutor Schottky (Aula 14 | Lista 3 - Questões 1, 2 e 3)",
            fontsize=12, fontweight="bold", color="#facc15"
        )

    anim = FuncAnimation(fig, update, frames=len(va_vals), interval=120)
    out_path = os.path.join(OUT_DIR, "anim_4_diodo_schottky.gif")
    anim.save(out_path, writer=PillowWriter(fps=8))
    plt.close(fig)
    print(f"Salvo: {out_path}")


def anim_5_capacitor_mos_regimes():
    """
    Animação 5: Capacitor MOS (Substrato Tipo P) varrendo Acumulação -> Banda Plana -> Depleção -> Inversão Forte.
    Ilustra a Aula 14 (Slides 7–19) e as Questões 4, 5, 6 e 7 da Lista 3.
    """
    print("Gerando anim_5_capacitor_mos_regimes.gif ...")
    fig, (ax_band, ax_cv) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=100)
    fig.subplots_adjust(wspace=0.28, top=0.83, bottom=0.14)

    # Parâmetros baseados na Questão 7 (e 5, 6) da Lista 3:
    # Substrato Tipo P: V_FB = -0.8 V, V_T = +0.25 V (Questão 6!), C_ox = 9 mF/m^2, C_min(HF) = 3 mF/m^2 (Questão 7!)
    V_FB = -0.80
    V_T = 0.25
    phi_F = 0.357  # V (Questão 5: NA = 10^16 cm^-3)
    Cox = 9.0      # mF/m^2 (Questão 7)
    Cmin = 3.0     # mF/m^2 (Questão 7)

    vg_grid = np.linspace(-2.5, 2.5, 400)
    c_hf = np.zeros_like(vg_grid)
    c_lf = np.zeros_like(vg_grid)
    for i, vg in enumerate(vg_grid):
        if vg <= V_FB:
            c_hf[i] = Cox
            c_lf[i] = Cox
        elif vg <= V_T:
            frac = (vg - V_FB) / (V_T - V_FB)
            # 1/C = 1/Cox + wd/eps_s
            inv_c = (1.0 / Cox) + frac * ((1.0 / Cmin) - (1.0 / Cox))
            c_hf[i] = 1.0 / inv_c
            c_lf[i] = c_hf[i]
        else:
            c_hf[i] = Cmin
            # Em LF a capacitância retorna a Cox na inversão forte
            c_lf[i] = Cmin + (Cox - Cmin) * (1.0 - np.exp(-(vg - V_T) / 0.18))

    vg_anim = np.concatenate([
        np.linspace(-2.0, -0.80, 12),
        np.full(4, -0.80),
        np.linspace(-0.80, 0.25, 14),
        np.full(4, 0.25),
        np.linspace(0.25, 2.0, 14),
        np.full(6, 2.0),
    ])

    x_semi = np.linspace(0.0, 1.2, 200)

    def update(frame):
        VG = vg_anim[frame]
        ax_band.clear()
        ax_cv.clear()
        ax_band.grid(True)
        ax_cv.grid(True)

        # Cálculo do potencial de superfície phi_s e queda no óxido V_ox
        if VG < V_FB:
            regime = "ACUMULAÇÃO DE LACUNAS ($V_G < V_{FB}$)"
            cor_reg = "#38bdf8"
            phi_s = 0.08 * np.tanh((VG - V_FB) / 0.6)  # ~ desprezível
        elif abs(VG - V_FB) < 0.03:
            regime = "BANDA PLANA ($V_G = V_{FB} \\Rightarrow \\varphi_s = 0$)"
            cor_reg = "#facc15"
            phi_s = 0.0
        elif VG < V_T:
            regime = "DEPLEÇÃO ($V_{FB} < V_G < V_T \\Rightarrow 0 < \\varphi_s < 2\\varphi_F$)"
            cor_reg = "#f472b6"
            phi_s = (2.0 * phi_F) * ((VG - V_FB) / (V_T - V_FB))
        else:
            regime = "INVERSÃO FORTE DE ELÉTRONS ($V_G > V_T \\Rightarrow \\varphi_s \\approx 2\\varphi_F$)"
            cor_reg = "#10b981"
            phi_s = 2.0 * phi_F + 0.03 * np.tanh((VG - V_T) / 0.8)

        V_ox = (VG - V_FB) - phi_s

        # Painel 1: Diagrama de Bandas do Capacitor MOS (Substrato Tipo P)
        # No volume (x -> 1.2): EF = 0, Ei = +phi_F, Ec = Ei + 0.56, Ev = Ei - 0.56
        EF_semi = 0.0
        Ei_bulk = phi_F
        w_dep = 0.15 if phi_s <= 0 else 0.75 * np.sqrt(phi_s / (2.0 * phi_F))
        bending = np.zeros_like(x_semi)
        if phi_s <= 0:
            bending = phi_s * np.exp(-x_semi / 0.12)
        else:
            m = x_semi <= w_dep
            bending[m] = phi_s * ((w_dep - x_semi[m]) / w_dep) ** 2

        Ei = Ei_bulk - bending
        Ec = Ei + 0.56
        Ev = Ei - 0.56

        # Região do Óxido (-0.25 <= x <= 0) e Porta Metálica (-0.55 <= x <= -0.25)
        ax_band.axvspan(-0.55, -0.25, color="#94a3b8", alpha=0.35, label="Porta (Gate)")
        ax_band.axvspan(-0.25, 0.0, color="#f59e0b", alpha=0.25, label="Óxido $\\mathrm{SiO}_2$ ($t_{ox}$)")
        EF_gate = -VG
        ax_band.hlines(EF_gate, -0.55, -0.25, color="#facc15", lw=3.0, label=f"$E_{{Fm}}$ ($V_G = {VG:+.2f}$ V)")
        # Inclinação da banda do óxido mostra o campo elétrico no óxido!
        ax_band.plot([-0.25, 0.0], [Ec[0] + 1.2 - V_ox * 0.6, Ec[0] + 1.2], color="#f59e0b", lw=2.2)

        ax_band.plot(x_semi, Ec, color="#38bdf8", lw=2.5, label="$E_C$ (Substrato P)")
        ax_band.plot(x_semi, Ei, color="#94a3b8", ls=":", lw=1.5, label="$E_i$")
        ax_band.plot(x_semi, Ev, color="#f472b6", lw=2.5, label="$E_V$")
        ax_band.hlines(EF_semi, 0.0, 1.2, color="#10b981", ls="--", lw=1.8, label="$E_F$ (Substrato)")

        ax_band.set_xlim(-0.55, 1.2)
        ax_band.set_ylim(-2.2, 2.3)
        ax_band.set_title(f"1. Bandas do Capacitor MOS ($\\varphi_s = {phi_s:+.2f}$ V, $2\\varphi_F = {2*phi_F:.2f}$ V)", fontsize=10.5)
        ax_band.set_xlabel("Posição (Porta | $\\mathrm{SiO}_2$ | Substrato Tipo P)")
        ax_band.set_ylabel("Energia dos Elétrons $E$ (eV)")
        ax_band.legend(loc="lower right", fontsize=7.5, facecolor="#0f172a")

        # Painel 2: Curva C-V (LF e HF) — Questão 7 da Lista 3
        ax_cv.plot(vg_grid, c_lf, color="#38bdf8", ls="--", lw=2.2, label="Baixa Frequência (LF): $C_{inv} = C_{ox}$")
        ax_cv.plot(vg_grid, c_hf, color="#10b981", lw=2.6, label="Alta Frequência (HF): $C_{inv} = 3$ mF/m$^2$")

        c_atual_hf = np.interp(VG, vg_grid, c_hf)
        ax_cv.scatter([VG], [c_atual_hf], color="#facc15", s=85, zorder=6)
        ax_cv.scatter([-2.0, 2.0], [9.0, 3.0], color="#f43f5e", s=70, zorder=5, label="Pontos da Questão 7 (Lista 3)")
        ax_cv.axvline(V_FB, color="#facc15", ls=":", lw=1.2)
        ax_cv.axvline(V_T, color="#10b981", ls=":", lw=1.2)
        ax_cv.text(V_FB - 0.35, 1.2, "$V_{FB}$", color="#facc15", fontweight="bold")
        ax_cv.text(V_T + 0.08, 1.2, "$V_T = 0,25$ V", color="#10b981", fontweight="bold")

        ax_cv.annotate("Acumulação ($V_G=-2$ V)\n$C_{ox}=9$ mF/m$^2 \\Rightarrow t_{ox}=3,84$ nm",
                       xy=(-2.0, 9.0), xytext=(-2.4, 6.2),
                       color="#38bdf8", fontweight="bold", fontsize=8.5,
                       arrowprops=dict(arrowstyle="->", color="#38bdf8"))
        ax_cv.annotate("Inversão Forte HF ($V_G=+2$ V)\n$C_{HF}=3$ mF/m$^2$",
                       xy=(2.0, 3.0), xytext=(0.55, 4.8),
                       color="#10b981", fontweight="bold", fontsize=8.5,
                       arrowprops=dict(arrowstyle="->", color="#10b981"))

        ax_cv.set_xlim(-2.5, 2.5)
        ax_cv.set_ylim(0.5, 10.5)
        ax_cv.set_title(f"2. Curva C–V do Capacitor MOS (Lista 3 - Q7): $C(V_G) = {c_atual_hf:.2f}$ mF/m$^2$", fontsize=10.5)
        ax_cv.set_xlabel("Tensão de Porta $V_G$ (V)")
        ax_cv.set_ylabel("Capacitância por Área $C$ (mF/m$^2$)")
        ax_cv.legend(loc="lower left", fontsize=8, facecolor="#0f172a")

        fig.suptitle(
            f"Capacitor MOS Tipo P (Aula 14 | Lista 3 - Q4 a Q7)\n{regime}",
            fontsize=11.5, fontweight="bold", color=cor_reg
        )

    anim = FuncAnimation(fig, update, frames=len(vg_anim), interval=120)
    out_path = os.path.join(OUT_DIR, "anim_5_capacitor_mos_regimes.gif")
    anim.save(out_path, writer=PillowWriter(fps=8))
    plt.close(fig)
    print(f"Salvo: {out_path}")


if __name__ == "__main__":
    anim_1_juncao_pn_eletrostatica()
    anim_2_injecao_correntes_pn()
    anim_3_capacitancia_deplecao()
    anim_4_diodo_schottky()
    anim_5_capacitor_mos_regimes()
    print("\nTodas as 5 animações GIF foram geradas com sucesso!")
