# components/lineup.py

import streamlit as st


def render_lineup_panel(
    position_options,
    bats_options,
    player_role_options,
):
    """
    Lineup Manager
    """

    with st.expander("📝 Lineup / PH / Subs", expanded=False):

        for i in range(len(st.session_state.lineup)):

            player = st.session_state.lineup[i]

            st.markdown(f"### Spot {i + 1}")

            c1, c2, c3 = st.columns([2.5, 1, 1])

            with c1:

                player["name"] = st.text_input(
                    "Starter",
                    value=player.get("name", ""),
                    key=f"starter_{i}",
                    placeholder="Player name",
                )

            with c2:

                current = player.get("position", "")

                player["position"] = st.selectbox(
                    "POS",
                    position_options,
                    index=position_options.index(current)
                    if current in position_options
                    else 0,
                    key=f"pos_{i}",
                )

            with c3:

                bats = player.get("bats", "")

                player["bats"] = st.selectbox(
                    "Bats",
                    bats_options,
                    index=bats_options.index(bats)
                    if bats in bats_options
                    else 0,
                    key=f"bats_{i}",
                )

            # -------------------------
            # Pinch Hitters / Subs
            # -------------------------

            if st.button(
                "➕ Add PH / Sub",
                key=f"add_sub_{i}",
                use_container_width=True,
            ):

                player["subs"].append(
                    {
                        "name": "",
                        "role": "PH",
                        "inning": "",
                        "position": "",
                    }
                )

                st.rerun()

            for s_idx, sub in enumerate(player["subs"]):

                sc1, sc2, sc3, sc4, sc5 = st.columns(
                    [2, 1, 1, 1, .6]
                )

                with sc1:

                    sub["name"] = st.text_input(
                        "Name",
                        value=sub.get("name", ""),
                        key=f"sub_name_{i}_{s_idx}",
                    )

                with sc2:

                    role = sub.get("role", "PH")

                    sub["role"] = st.selectbox(
                        "Role",
                        player_role_options,
                        index=player_role_options.index(role)
                        if role in player_role_options
                        else 0,
                        key=f"sub_role_{i}_{s_idx}",
                    )

                with sc3:

                    sub["inning"] = st.text_input(
                        "Inn",
                        value=sub.get("inning", ""),
                        key=f"sub_inning_{i}_{s_idx}",
                    )

                with sc4:

                    pos = sub.get("position", "")

                    sub["position"] = st.selectbox(
                        "POS",
                        position_options,
                        index=position_options.index(pos)
                        if pos in position_options
                        else 0,
                        key=f"sub_pos_{i}_{s_idx}",
                    )

                with sc5:

                    if st.button(
                        "❌",
                        key=f"remove_sub_{i}_{s_idx}",
                        use_container_width=True,
                    ):

                        player["subs"].pop(s_idx)

                        st.rerun()

            st.divider()