import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns


class WorldCupAnalyticsApp:
    """Dynamic FIFA World Cup 2026 Analytics Dashboard for any selected team."""

    # FIFA ratings dictionary covering World Cup 2026 teams
    FIFA_RATINGS = {
        'Argentina': 1850, 'France': 1840, 'Spain': 1810, 'England': 1800, 'Brazil': 1790,
        'Belgium': 1750, 'Netherlands': 1740, 'Portugal': 1730, 'Colombia': 1700, 'Italy': 1690,
        'Uruguay': 1680, 'Germany': 1670, 'Croatia': 1650, 'Japan': 1620, 'Morocco': 1610,
        'United States': 1600, 'Mexico': 1580, 'Senegal': 1570, 'Austria': 1560, 'Switzerland': 1550,
        'South Korea': 1530, 'Australia': 1500, 'Ecuador': 1490, 'Türkiye': 1480, 'Canada': 1470,
        'Norway': 1460, 'Algeria': 1450, 'Egypt': 1440, 'Ivory Coast': 1430, 'Côte d’Ivoire': 1430,
        'Nigeria': 1420, 'Czechia': 1410, 'Saudi Arabia': 1400, 'Ghana': 1390, 'Qatar': 1380,
        'Iraq': 1350, 'Uzbekistan': 1340, 'South Africa': 1330, 'Jordan': 1320,
        'Bosnia & Herzegovina': 1310, 'Haiti': 1250, 'Curacao': 1240, 'Curaçao': 1240,
        'Cape Verde': 1230, 'New Zealand': 1220, 'Congo - Kinshasa': 1210, 'Panama': 1200,
        'Sweden': 1540, 'Paraguay': 1430, 'Tunisia': 1420
    }

    def __init__(self, filepath=r'C:\Users\GG Store\Downloads\New folder\world-cup-2026-team-schedules.csv'):
        self.df = pd.read_csv(filepath)
        self.available_teams = sorted(self.df['team_name'].dropna().unique().tolist())

    def _get_rating(self, team_name: str) -> int:
        return self.FIFA_RATINGS.get(team_name, 1400)

    def draw_pitch(self, ax, title: str):
        ax.set_facecolor('#0f172a')
        ax.add_patch(patches.Rectangle((0, 0), 120, 80, fill=False, edgecolor='#94a3b8', lw=2))
        ax.plot([60, 60], [0, 80], color='#94a3b8', lw=1.5)
        ax.add_patch(patches.Circle((60, 40), 9.15, fill=False, edgecolor='#94a3b8', lw=1.5))
        ax.add_patch(patches.Rectangle((0, 18), 18, 44, fill=False, edgecolor='#94a3b8', lw=1.5))
        ax.add_patch(patches.Rectangle((102, 18), 18, 44, fill=False, edgecolor='#94a3b8', lw=1.5))
        ax.add_patch(patches.Rectangle((0, 30), 6, 20, fill=False, edgecolor='#94a3b8', lw=1.5))
        ax.add_patch(patches.Rectangle((114, 30), 6, 20, fill=False, edgecolor='#94a3b8', lw=1.5))
        
        ax.set_xlim(-5, 125)
        ax.set_ylim(-5, 85)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=12, color='white', fontweight='bold', pad=10)

    def generate_telemetry(self, team_name: str, opponent_name: str):
        """Generates pass vectors and shot locations based on relative team strength."""
        np.random.seed(abs(hash(team_name + opponent_name)) % (2**32))
        rating_diff = self._get_rating(team_name) - self._get_rating(opponent_name)
        
        # Pass Telemetry
        num_passes = int(max(200, np.random.normal(450 + rating_diff * 0.2, 40)))
        px = np.random.beta(6, 3, num_passes) * 120
        py = np.clip(np.random.normal(40, 16, num_passes), 5, 75)
        p_end_x = np.clip(px + np.random.normal(10, 8, num_passes), 0, 120)
        p_end_y = np.clip(py + np.random.normal(0, 8, num_passes), 0, 80)
        passes_df = pd.DataFrame({'x': px, 'y': py, 'end_x': p_end_x, 'end_y': p_end_y})

        # Shot Telemetry & xG Math
        num_shots = int(max(3, np.random.poisson(max(0.5, 1.4 + rating_diff / 400.0) * 7)))
        sx = np.random.beta(8, 2, num_shots) * 28 + 92
        sy = np.clip(np.random.normal(40, 10, num_shots), 20, 60)
        dist = np.sqrt((120 - sx)**2 + (40 - sy)**2)
        xg = np.exp(-0.14 * dist)
        is_goal = xg > np.random.uniform(0.2, 0.7, num_shots)
        shots_df = pd.DataFrame({'x': sx, 'y': sy, 'xg': xg, 'is_goal': is_goal})

        return passes_df, shots_df

    def simulate_win_probabilities(self, team_name: str, num_sims: int = 10000) -> pd.DataFrame:
        """Runs a 10,000 match Monte Carlo simulation for all group stage matches."""
        team_matches = self.df[self.df['team_name'] == team_name].drop_duplicates(subset=['match_id'])
        results = []

        for _, row in team_matches.iterrows():
            opp = row['opponent_name']
            r_team = self._get_rating(team_name) + (50 if row['is_home'] else 0)
            r_opp = self._get_rating(opp)

            diff = r_team - r_opp
            lam_team = max(0.4, 1.4 + (diff / 350.0))
            lam_opp = max(0.4, 1.2 - (diff / 350.0))

            t_goals = np.random.poisson(lam_team, num_sims)
            o_goals = np.random.poisson(lam_opp, num_sims)

            results.append({
                'Opponent': opp,
                'Win %': round(np.sum(t_goals > o_goals) / num_sims * 100, 1),
                'Draw %': round(np.sum(t_goals == o_goals) / num_sims * 100, 1),
                'Loss %': round(np.sum(t_goals < o_goals) / num_sims * 100, 1)
            })

        return pd.DataFrame(results)

    def plot_dashboard(self, team_name: str):
        """Displays the tactical dashboard for the requested team."""
        team_matches = self.df[self.df['team_name'] == team_name]
        if team_matches.empty:
            print(f"[-] Team '{team_name}' not found in schedule dataset.")
            return

        first_opp = team_matches.iloc[0]['opponent_name']
        passes_df, shots_df = self.generate_telemetry(team_name, first_opp)
        probs_df = self.simulate_win_probabilities(team_name)

        fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor='#111827')

        # 1. Positional Heatmap
        self.draw_pitch(axes[0, 0], f"{team_name} - Heatmap (vs {first_opp})")
        sns.kdeplot(data=passes_df, x='x', y='y', cmap='magma', fill=True, thresh=0.05, alpha=0.7, ax=axes[0, 0])

        # 2. Passing Vectors
        self.draw_pitch(axes[0, 1], f"{team_name} - Pass Vectors (vs {first_opp})")
        for _, p in passes_df.sample(min(50, len(passes_df)), random_state=42).iterrows():
            axes[0, 1].annotate(
                '', xy=(p['end_x'], p['end_y']), xytext=(p['x'], p['y']),
                arrowprops=dict(arrowstyle='->', color='#38bdf8', lw=1.2, alpha=0.8)
            )

        # 3. Shot Map & xG
        self.draw_pitch(axes[1, 0], f"{team_name} - Shot Map & xG (vs {first_opp})")
        non_goals = shots_df[~shots_df['is_goal']]
        goals = shots_df[shots_df['is_goal']]
        axes[1, 0].scatter(non_goals['x'], non_goals['y'], s=non_goals['xg']*400 + 60, c='#f87171', alpha=0.8, edgecolors='white', label='Shot (Miss/Save)')
        axes[1, 0].scatter(goals['x'], goals['y'], s=goals['xg']*600 + 120, c='#facc15', marker='*', edgecolors='black', label='Goal')
        axes[1, 0].legend(loc='lower left', facecolor='#1e293b', edgecolor='white', labelcolor='white')

        # 4. Win Probabilities Bar Chart
        axes[1, 1].set_facecolor('#0f172a')
        x = np.arange(len(probs_df))
        w = 0.25

        r1 = axes[1, 1].bar(x - w, probs_df['Win %'], w, label='Win %', color='#4ade80')
        r2 = axes[1, 1].bar(x, probs_df['Draw %'], w, label='Draw %', color='#facc15')
        r3 = axes[1, 1].bar(x + w, probs_df['Loss %'], w, label='Loss %', color='#f87171')

        axes[1, 1].set_ylabel('Probability (%)', color='white', fontsize=11)
        axes[1, 1].set_title(f'{team_name} - World Cup 2026 Win Probabilities', color='white', fontsize=12, fontweight='bold', pad=10)
        axes[1, 1].set_xticks(x)
        axes[1, 1].set_xticklabels([f"vs {o}" for o in probs_df['Opponent']], color='white', fontsize=11)
        axes[1, 1].tick_params(colors='white')
        axes[1, 1].legend(facecolor='#1e293b', edgecolor='white', labelcolor='white')
        axes[1, 1].set_ylim(0, 100)

        for rect in r1 + r2 + r3:
            h = rect.get_height()
            axes[1, 1].annotate(f'{h}%', xy=(rect.get_x() + rect.get_width() / 2, h),
                                xytext=(0, 3), textcoords="offset points",
                                ha='center', va='bottom', color='white', fontsize=9)

        plt.tight_layout()
        plt.show()

    def run(self):
        print("=" * 65)
        print("    FIFA WORLD CUP 2026 - INTERACTIVE TEAM ANALYTICS APP    ")
        print("=" * 65)
        
        while True:
            print(f"\nAvailable Teams ({len(self.available_teams)} total):")
            print(", ".join(self.available_teams[:12]) + "...")
            
            user_input = input("\nEnter a team name (or type 'list' to see all, 'exit' to quit): ").strip()
            
            if user_input.lower() == 'exit':
                print("Exiting application. Goodbye!")
                break
            elif user_input.lower() == 'list':
                print("\nAll 48 World Cup 2026 Teams:")
                for i in range(0, len(self.available_teams), 4):
                    print("  ".join(f"{t:<22}" for t in self.available_teams[i:i+4]))
                continue

            # Fuzzy / exact matching
            matched_teams = [t for t in self.available_teams if t.lower() == user_input.lower()]
            if matched_teams:
                team = matched_teams[0]
                print(f"\n[+] Processing World Cup analytics for {team}...")
                self.plot_dashboard(team)
            else:
                partial_matches = [t for t in self.available_teams if user_input.lower() in t.lower()]
                if partial_matches:
                    print(f"[-] Team '{user_input}' not found. Did you mean: {', '.join(partial_matches)}?")
                else:
                    print(f"[-] Team '{user_input}' not found. Try typing 'list' to view available teams.")


if __name__ == "__main__":
    app = WorldCupAnalyticsApp()
    app.run()