def write_gif(total):

    from PIL import Image, ImageDraw

    ASSETS.mkdir(
        parents=True,
        exist_ok=True
    )

    WIDTH = 900
    HEIGHT = 320

    FOOD_COLOR = "#22c55e"
    SNAKE_COLOR = "#14b8a6"
    HEAD_COLOR = "#2dd4bf"
    BG_COLOR = "#0d1117"
    BOARD_COLOR = "#161b22"
    BORDER_COLOR = "#30363d"
    TEXT_COLOR = "#f0f6fc"
    MUTED_COLOR = "#8b949e"

    # --------------------------------------------------
    # No solutions yet
    # --------------------------------------------------

    if total == 0:

        image = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            BG_COLOR
        )

        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle(
            (30, 80, 870, 270),
            radius=18,
            fill=BOARD_COLOR,
            outline=BORDER_COLOR,
            width=2
        )

        draw.text(
            (40, 25),
            "🐍 GFG Solution Snake",
            fill=TEXT_COLOR
        )

        draw.text(
            (40, 55),
            "Solve a GFG problem to spawn food.",
            fill=MUTED_COLOR
        )

        draw.text(
            (40, 285),
            "Solutions tracked: 0",
            fill=MUTED_COLOR
        )

        image.save(
            ASSETS / "gfg-solution-snake.gif"
        )

        return

    # --------------------------------------------------
    # Generate food positions
    # --------------------------------------------------

    points = path_points(
        total,
        width=760,
        height=170
    )

    # Move points slightly so the board looks cleaner
    points = [
        (x + 70, y + 85)
        for x, y in points
    ]

    frames = []

    # --------------------------------------------------
    # Create frames
    # --------------------------------------------------

    snake = []

    start_position = (
        70,
        HEIGHT // 2
    )

    current_position = start_position

    # Number of body segments the snake gains
    # after eating each solution
    GROWTH = 5

    # --------------------------------------------------
    # Draw a single frame
    # --------------------------------------------------

    def draw_frame(
        food,
        snake_body,
        head_position,
        eaten_count
    ):

        image = Image.new(
            "RGB",
            (WIDTH, HEIGHT),
            BG_COLOR
        )

        draw = ImageDraw.Draw(
            image
        )

        # Title
        draw.text(
            (40, 20),
            "🐍 GFG Solution Snake",
            fill=TEXT_COLOR
        )

        draw.text(
            (40, 50),
            "🟢 = GFG solution",
            fill=MUTED_COLOR
        )

        # Game board
        draw.rounded_rectangle(
            (30, 80, 870, 270),
            radius=18,
            fill=BOARD_COLOR,
            outline=BORDER_COLOR,
            width=2
        )

        # ------------------------------------------
        # Draw remaining food
        # ------------------------------------------

        for food_x, food_y in food:

            r = 8

            draw.ellipse(
                (
                    food_x - r,
                    food_y - r,
                    food_x + r,
                    food_y + r
                ),
                fill=FOOD_COLOR
            )

            # Small highlight
            draw.ellipse(
                (
                    food_x - 3,
                    food_y - 5,
                    food_x,
                    food_y - 2
                ),
                fill="#86efac"
            )

        # ------------------------------------------
        # Draw snake body
        # ------------------------------------------

        for index, (
            segment_x,
            segment_y
        ) in enumerate(
            snake_body
        ):

            radius = max(
                6,
                12 - index * 0.35
            )

            draw.ellipse(
                (
                    segment_x - radius,
                    segment_y - radius,
                    segment_x + radius,
                    segment_y + radius
                ),
                fill=SNAKE_COLOR
            )

        # ------------------------------------------
        # Draw snake head
        # ------------------------------------------

        head_x, head_y = head_position

        radius = 14

        draw.ellipse(
            (
                head_x - radius,
                head_y - radius,
                head_x + radius,
                head_y + radius
            ),
            fill=HEAD_COLOR,
            outline="#d1fae5",
            width=2
        )

        # Eyes
        draw.ellipse(
            (
                head_x + 3,
                head_y - 6,
                head_x + 6,
                head_y - 3
            ),
            fill=BG_COLOR
        )

        # ------------------------------------------
        # Progress
        # ------------------------------------------

        draw.text(
            (40, 285),
            f"Solutions eaten: {eaten_count} / {total}",
            fill=MUTED_COLOR
        )

        return image

    # --------------------------------------------------
    # Initial snake
    # --------------------------------------------------

    snake = [
        (
            start_position[0] - i * 12,
            start_position[1]
        )
        for i in range(4)
    ]

    # --------------------------------------------------
    # Animate each solution being eaten
    # --------------------------------------------------

    remaining_food = list(points)

    for food_index, target in enumerate(points):

        target_x, target_y = target

        start_x, start_y = current_position

        # ------------------------------------------
        # Calculate movement
        # ------------------------------------------

        distance = math.sqrt(
            (target_x - start_x) ** 2
            + (target_y - start_y) ** 2
        )

        steps = max(
            10,
            int(distance / 12)
        )

        # ------------------------------------------
        # Move snake toward food
        # ------------------------------------------

        for step in range(
            steps
        ):

            progress = (
                step + 1
            ) / steps

            head_x = (
                start_x
                + (target_x - start_x)
                * progress
            )

            head_y = (
                start_y
                + (target_y - start_y)
                * progress
            )

            head = (
                head_x,
                head_y
            )

            # Add new head
            snake.insert(
                0,
                head
            )

            # Keep current length
            max_length = (
                5
                + (food_index * GROWTH)
            )

            snake = snake[
                :max_length
            ]

            frames.append(
                draw_frame(
                    remaining_food,
                    snake[1:],
                    head,
                    food_index
                )
            )

        # ------------------------------------------
        # FOOD HAS BEEN EATEN
        # ------------------------------------------

        if target in remaining_food:

            remaining_food.remove(
                target
            )

        # ------------------------------------------
        # Eating animation
        # ------------------------------------------

        for _ in range(4):

            frames.append(
                draw_frame(
                    remaining_food,
                    snake[1:],
                    snake[0],
                    food_index + 1
                )
            )

        current_position = target

    # --------------------------------------------------
    # Hold final frame
    # --------------------------------------------------

    final_frame = draw_frame(
        remaining_food,
        snake[1:],
        snake[0],
        total
    )

    for _ in range(12):

        frames.append(
            final_frame.copy()
        )

    # --------------------------------------------------
    # Save GIF
    # --------------------------------------------------

    frames[0].save(
        ASSETS / "gfg-solution-snake.gif",
        save_all=True,
        append_images=frames[1:],
        duration=70,
        loop=0,
        disposal=2
    )
