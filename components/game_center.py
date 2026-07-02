import streamlit as st

from components.header import render_game_center_header
from database import load_games, delete_game


def render_game_center(new_game_callback, open_game_callback):
    """
    Main Game Center screen.
    """

    render_game_center_header()

    c1, c2 = st.columns([3, 1])

    with c1:
        if st.button(
            "➕ New Game",
            key="gc_new_game",
            use_container_width=True,
        ):
            new_game_callback()

    with c2:
        st.metric(
            "Saved Games",
            len(load_games())
        )

    st.divider()

    games = load_games()

    if not games:
        st.info("No saved games yet.")
        return

    sorted_games = sorted(
        games.values(),
        key=lambda g: g.get("saved_at", ""),
        reverse=True,
    )

    for game in sorted_games:

        game_id = game["game_id"]
        info = game["game_info"]

        with st.container(border=True):

            top_left, top_right = st.columns([3, 1])

            with top_left:

                st.subheader(
                    f"{info.get('team','Team')} vs {info.get('opponent','Opponent')}"
                )

                chips = []

                if info.get("date"):
                    chips.append(f"📅 {info['date']}")

                if info.get("home_away"):
                    chips.append(f"🏟️ {info['home_away']}")

                if info.get("game_number"):
                    chips.append(f"⚾ Game {info['game_number']}")

                if info.get("score"):
                    chips.append(f"📊 {info['score']}")

                st.caption(" • ".join(chips))

            with top_right:

                st.caption("Last Saved")

                st.write(
                    game.get("saved_at", "")
                )

            b1, b2 = st.columns(2)

            with b1:

                if st.button(
                    "▶ Continue",
                    key=f"open_{game_id}",
                    use_container_width=True,
                ):
                    open_game_callback(game_id)

            with b2:

                if st.button(
                    "🗑 Delete",
                    key=f"delete_{game_id}",
                    use_container_width=True,
                ):
                    delete_game(game_id)
                    st.rerun()

        st.write("")