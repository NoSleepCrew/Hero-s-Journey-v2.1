"""One-off Chronicle UI screenshots. Run: python capture.py"""
import os
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.dirname(os.path.abspath(__file__))
URL = "file:///" + BASE.replace("\\", "/").replace(" ", "%20") + "/index.html"

def main():
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 900})
        page.goto(URL, wait_until="load", timeout=60000)
        page.wait_for_timeout(2500)
        page.evaluate("""
            localStorage.setItem('hj_seen_achievements', JSON.stringify(getAchievementDefs().filter(a=>a.done).map(a=>a.id)));
            localStorage.setItem('hj_seen_deed_milestones', JSON.stringify([5,10,15,20,25,30,40,50]));
            closeCelebration();
        """)
        page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(OUT, "01-dragon-dashboard.png"), full_page=False)

        page.evaluate("""
            document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
            document.getElementById('kingdom').classList.add('active');
            document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));
            document.getElementById('nav-kingdom').classList.add('active');
            renderKingdomSanctum();
        """)
        page.wait_for_timeout(1200)
        page.screenshot(path=os.path.join(OUT, "02-sanctum-restoring.png"), full_page=True)

        page.evaluate("""
            state.books=12; state.meals=20; state.language=28; state.coop=15;
            state.habitLadders.riseAndShine=85; state.habitLadders.firstChapter=120;
            state.unlockedTitles=['riseAndShine']; state.equippedTitleId='riseAndShine';
            save();
        """)
        page.wait_for_timeout(1500)
        page.screenshot(path=os.path.join(OUT, "03-sanctum-progress.png"), full_page=True)

        page.evaluate("""
            state.books=200; state.meals=100; state.language=100; state.coop=50;
            state.legend=true; state.chronicleLegendRevealed=true;
            save();
        """)
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(OUT, "04-sanctum-complete.png"), full_page=True)

        page.evaluate("openChronicleReveal()")
        page.wait_for_timeout(800)
        page.screenshot(path=os.path.join(OUT, "05-legend-reveal.png"), full_page=False)

        browser.close()
    print("Screenshots saved to", OUT)

if __name__ == "__main__":
    main()
