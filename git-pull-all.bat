@echo off
echo ====================================
echo Git Pull Script for TAC Directories
echo ====================================
echo.

set "BASE_DIR=C:\Users\Split Lease\splitleaseteam\!Agent Context and Tools\SL1\tac1THRU8"

echo [1/8] Pulling tac-4\app...
cd "%BASE_DIR%\tac-4\app"
git pull
echo.

echo [2/8] Pulling tac-5\app...
cd "%BASE_DIR%\tac-5\app"
git pull
echo.

echo [3/8] Pulling tac-6\app...
cd "%BASE_DIR%\tac-6\app"
git pull
echo.

echo [4/8] Pulling tac-7\app...
cd "%BASE_DIR%\tac-7\app"
git pull
echo.

echo [5/8] Pulling tac-8\tac8_app1__agent_layer_primitives\apps...
cd "%BASE_DIR%\tac-8\tac8_app1__agent_layer_primitives\apps"
git pull
echo.

echo [6/8] Pulling tac-8\tac8_app2__multi_agent_todone\apps...
cd "%BASE_DIR%\tac-8\tac8_app2__multi_agent_todone\apps"
git pull
echo.

echo [7/8] Pulling tac-8\tac8_app3__out_loop_multi_agent_task_board\apps...
cd "%BASE_DIR%\tac-8\tac8_app3__out_loop_multi_agent_task_board\apps"
git pull
echo.

echo [8/8] Pulling tac-8\tac8_app4__agentic_prototyping\splitlease...
cd "%BASE_DIR%\tac-8\tac8_app4__agentic_prototyping\splitlease"
git pull
echo.

echo ====================================
echo All git pull operations completed!
echo ====================================
pause
