#!/usr/bin/env python3
import os
import re

# ---------------------------
OUTPUT_PATH = "./TD_results" # Path
os.makedirs(OUTPUT_PATH, exist_ok=True)

# ---------------------------
MAX_STATES = 10  # Max number of states

# ---------------------------
logs = [f for f in os.listdir('.') if f.endswith(".log")]
if not logs:
    print("No .log file found.")
    exit()

for logfile in logs:
    transitions_all = []
    print(f"\n--- Reading : {logfile} ---")

    homo = None
    lumo = None
    singlet = False

    # ---------------------
    # Spin state and HOMO/LUMO information
    with open(logfile, 'r', errors="ignore") as f:
        for line in f:
            m_spin = re.match(r'\s*(\d+)\s+alpha electrons\s+(\d+)\s+beta electrons', line)
            if m_spin:
                alpha = int(m_spin.group(1))
                beta = int(m_spin.group(2))
                if alpha == beta:
                    singlet = True
                homo = alpha  # HOMO = last occupied orbital
                lumo = homo + 1
                break

    if singlet:
        print(f"Spin singlet: {singlet}, HOMO: {homo}, LUMO: {lumo}")
    else:
        print("Impossible to determine HOMO/LUMO")

    # ---------------------
    # Mapping HOMO/LUMO for singlet state
    orbital_map = {}
    if singlet:
        for i in range(1, homo+1):
            orbital_map[i] = f"HOMO-{homo-i}" if i != homo else "HOMO"
        for i in range(lumo, lumo + 100):  # Large enough to cover LUMO+...
            orbital_map[i] = f"LUMO+{i-lumo}" if i != lumo else "LUMO"

    # ---------------------
    # Parsing transitions
    with open(logfile, 'r', errors="ignore") as f:
        state_count = 0
        reading_transitions = False
        idx = sym = e_ev = wavelength = fval = None
        first_transition = True  # flag to avoid state

        for line in f:
            line_strip = line.strip()

            # ----- Starting Excited State reading -----
            if "Excited State" in line_strip:
                if state_count >= MAX_STATES:
                    break

                m_idx = re.search(r'Excited State\s+(\d+):', line_strip)
                idx = int(m_idx.group(1)) if m_idx else None

                m_sym = re.search(r':\s*(\S+)', line_strip)
                sym = m_sym.group(1) if m_sym else None

                m_ev = re.search(r'([\d.]+)\s*eV', line_strip)
                e_ev = float(m_ev.group(1)) if m_ev else None

                m_nm = re.search(r'([\d.]+)\s*nm', line_strip)
                wavelength = float(m_nm.group(1)) if m_nm else None

                m_f = re.search(r'f=([\d.eE+-]+)', line_strip)
                fval = float(m_f.group(1)) if m_f else None

                #print(f"State {idx} | Spin-Sym {sym} | E {e_ev:.2f} eV | λ {round(wavelength)} nm | f {fval}")
                reading_transitions = True
                first_transition = True
                state_count += 1
                continue

            # ----- Transitions (orbitals) -----
            if reading_transitions:
                m_trans = re.match(r'(\d+)\s*->\s*(\d+)\s+([-\d.eE]+)', line_strip)
                if m_trans:
                    start = int(m_trans.group(1))
                    end = int(m_trans.group(2))
                    coeff = float(m_trans.group(3))
                    percentage = round((coeff ** 2) * 2 * 100, )

                    # Replace orbital number by name (HOMO-x or LUMO+y)
                    if singlet:
                        start_name = orbital_map.get(start, start)
                        end_name = orbital_map.get(end, end)
                    else:
                        start_name = start
                        end_name = end

                    state_col = idx if first_transition else ""
                    first_transition = False

                    transitions_all.append([state_col, sym, round(e_ev,2), round(wavelength), round(fval,4), start_name, end_name, percentage])
                    #print(f"   Transition: {start_name} -> {end_name} | coeff={coeff:.5f} | %={percentage}")
                elif line_strip == "":
                    reading_transitions = False

    # ----- Writing the files -----
    base = os.path.splitext(logfile)[0]
    txt_file = os.path.join(OUTPUT_PATH, base + ".txt")
    csv_file = os.path.join(OUTPUT_PATH, base + "_pretty.csv")

    headers = ["State", "Spin-Sym", "E(eV)", "lambda(nm)", "f", "start", "end", "%"]
    col_widths = [6, 12, 10, 12, 8, 10, 10, 6]

    # TXT
    with open(txt_file, 'w') as t:
        header_line = "".join(f"{h:^{w}}" for h, w in zip(headers, col_widths))
        t.write(header_line + "\n")
        t.write("_" * sum(col_widths) + "\n")

        last_state = None
        for row in transitions_all:
            if row[0] != "" and row[0] != last_state:
                if last_state is not None:
                    t.write("-" * sum(col_widths) + "\n")
                last_state = row[0]

            line = "".join(f"{str(val):^{w}}" if isinstance(val, (int,float)) else f"{val:^{w}}" 
                           for val, w in zip(row, col_widths))
            t.write(line + "\n")

    print(f"writing {txt_file}")

print("\nAll log files have been treated.")
