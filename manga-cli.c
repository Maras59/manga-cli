#include <ncurses.h>
#include <stdio.h>
#include <stdlib.h>

void run_script(WINDOW *win) {
    FILE *pipe;
    char buffer[256];
    int y = 1;

    pipe = popen("./python/utils.py", "r");
    if (pipe == NULL) {
        mvwprintw(win, 1, 1, "Failed to run script.");
        wrefresh(win);
        return;
    }

    while (fgets(buffer, sizeof(buffer), pipe) != NULL) {
        mvwprintw(win, y, 1, "%s", buffer);
        wrefresh(win);
        y++;
    }

    pclose(pipe);
}

int main() {
    initscr();
    noecho();
    cbreak();
    curs_set(0);

    WINDOW *win = newwin(LINES - 2, COLS - 2, 1, 1);
    box(win, 0, 0);
    wrefresh(win);

    run_script(win);

    mvwprintw(win, LINES - 3, 2, "Press any key to exit...");
    wrefresh(win);
    getch();

    endwin();
    return 0;
}
