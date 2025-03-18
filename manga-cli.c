#include <ncurses.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

void run_script(WINDOW *win) {
    char buffer[256];
    int y = 1;

    char command[256];
    snprintf(command, sizeof(command), "python3 ./pyscripts/utils.py %d %d", LINES, COLS);

    // Open the pipe to run the command
    FILE *pipe = popen(command, "r");
    if (pipe == NULL) {
        mvwprintw(win, 1, 1, "Failed to run script: %s", strerror(errno));
        wrefresh(win);
        return;
    }

    while (fgets(buffer, sizeof(buffer), pipe) != NULL) {
        mvwprintw(win, y, 1, "%s", buffer);
        wrefresh(win);
        y++;
        usleep(100);  // Delay to slow down the drawing
    }

    // If no output is received from the Python script
    if (y == 1) {
        mvwprintw(win, 1, 1, "No output from script.");
        wrefresh(win);
    }

    pclose(pipe);
}

int main() {
    initscr();      
    noecho();  
    cbreak();       
    curs_set(0);    

    WINDOW *win = newwin(LINES - 2, COLS - 2, 0, 0);  
    wrefresh(win);

    run_script(win);

    mvwprintw(win, LINES - 3, 2, "Press any key to exit...");
    wrefresh(win); 

    nodelay(win, TRUE);

    int ch;
    while ((ch = wgetch(win)) == ERR) {
        usleep(50000);  // Adjust the delay as needed
    }

    refresh();

    endwin();

    printf("python3 ./pyscripts/utils.py %d %d\n", LINES, COLS);

    return 0;
}
