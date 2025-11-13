#!/bin/bash

# Frontend Modernization Testing Script - PR #1
# Interactive test runner with pass/fail tracking and summary

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Test tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
SKIPPED_TESTS=0

# Arrays to store results
declare -a FAILED_TEST_NAMES=()
declare -a PASSED_TEST_NAMES=()

# Server process ID
SERVER_PID=""

# Banner
print_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║     Ship Maintenance Tracker - Frontend Testing Suite         ║"
    echo "║                    PR #1 - v2.0.0                              ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Section header
print_section() {
    echo -e "\n${MAGENTA}${BOLD}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${MAGENTA}${BOLD}  $1${NC}"
    echo -e "${MAGENTA}${BOLD}═══════════════════════════════════════════════════════════${NC}\n"
}

# Test prompt
run_test() {
    local test_name="$1"
    local test_description="$2"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    echo -e "${BLUE}${BOLD}TEST ${TOTAL_TESTS}:${NC} ${test_name}"
    echo -e "${CYAN}Description:${NC} ${test_description}"
    echo -e ""
    
    # Prompt for result
    while true; do
        read -p "$(echo -e ${YELLOW}Result [p]ass / [f]ail / [s]kip: ${NC})" response
        case $response in
            [Pp]* )
                PASSED_TESTS=$((PASSED_TESTS + 1))
                PASSED_TEST_NAMES+=("$test_name")
                echo -e "${GREEN}✓ PASSED${NC}\n"
                break;;
            [Ff]* )
                FAILED_TESTS=$((FAILED_TESTS + 1))
                FAILED_TEST_NAMES+=("$test_name")
                read -p "$(echo -e ${RED}Notes on failure: ${NC})" failure_note
                echo -e "${RED}✗ FAILED${NC} - ${failure_note}\n"
                break;;
            [Ss]* )
                SKIPPED_TESTS=$((SKIPPED_TESTS + 1))
                echo -e "${YELLOW}⊘ SKIPPED${NC}\n"
                break;;
            * )
                echo -e "${RED}Invalid input. Please enter p, f, or s.${NC}";;
        esac
    done
}

# Start local server
start_server() {
    print_section "🚀 Server Setup"
    
    echo -e "${CYAN}Checking if server is already running...${NC}"
    if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${YELLOW}Server already running on port 5001${NC}"
        read -p "$(echo -e ${YELLOW}Use existing server? [y/n]: ${NC})" use_existing
        if [[ ! $use_existing =~ ^[Yy]$ ]]; then
            echo -e "${RED}Please stop the existing server and run this script again.${NC}"
            exit 1
        fi
    else
        echo -e "${CYAN}Starting Flask development server...${NC}"
        
        # Check if virtual environment exists
        if [ -d "venv" ]; then
            echo -e "${GREEN}Virtual environment found${NC}"
            source venv/bin/activate
        else
            echo -e "${YELLOW}No virtual environment found. Using system Python.${NC}"
        fi
        
        # Start server in background
        python run.py > /tmp/flask_test_server.log 2>&1 &
        SERVER_PID=$!
        
        echo -e "${CYAN}Waiting for server to start...${NC}"
        sleep 3
        
        # Check if server started successfully
        if lsof -Pi :5001 -sTCP:LISTEN -t >/dev/null ; then
            echo -e "${GREEN}✓ Server started successfully on http://localhost:5001${NC}"
            echo -e "${CYAN}Server PID: ${SERVER_PID}${NC}"
        else
            echo -e "${RED}✗ Server failed to start. Check /tmp/flask_test_server.log for errors${NC}"
            exit 1
        fi
    fi
    
    echo -e "\n${GREEN}Ready to begin testing!${NC}"
    read -p "$(echo -e ${YELLOW}Press Enter to continue...${NC})"
}

# Open browser
open_browser() {
    local url="$1"
    echo -e "${CYAN}Opening ${url} in browser...${NC}"
    
    # Detect OS and open browser
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$url"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open "$url"
    else
        echo -e "${YELLOW}Please manually open: ${url}${NC}"
    fi
    sleep 2
}

# Critical Bug Fixes Tests
test_critical_bugs() {
    print_section "🎯 Critical Bug Fixes (Test First!)"
    
    echo -e "${BOLD}Testing the two critical bug fixes from PR #1${NC}\n"
    
    # Bug Fix #1: Photo Preview
    echo -e "${YELLOW}Bug Fix #1: Photo Preview in Admin Dashboard${NC}"
    echo -e "Issue: Photos were not displaying in admin dashboard cards"
    echo -e "Fix: Changed route from admin.serve_upload to serve_upload\n"
    
    open_browser "http://localhost:5001/admin/login"
    echo -e "${CYAN}Login with: admin / admin67${NC}\n"
    
    run_test "Photo Preview - Admin Dashboard Cards" \
             "Navigate to admin dashboard. Do work item cards show photo thumbnails?"
    
    run_test "Photo Preview - Photo Count Badge" \
             "Check photo count badge on cards. Does it show correct number?"
    
    # Bug Fix #2: Dark Mode
    echo -e "${YELLOW}Bug Fix #2: Dark Mode Removal${NC}"
    echo -e "Issue: App was switching to dark mode based on system preferences"
    echo -e "Fix: Removed @media (prefers-color-scheme: dark) from variables.css\n"
    
    echo -e "${CYAN}Instructions:${NC}"
    echo -e "1. Enable Dark Mode in your system settings"
    echo -e "2. Refresh the browser"
    echo -e "3. Check if the app stays in light mode (white backgrounds)\n"
    
    run_test "Dark Mode - System Dark Mode Enabled" \
             "With system dark mode ON, does the app stay in light mode?"
}

# Login Pages Tests
test_login_pages() {
    print_section "🔐 Login Pages"
    
    # Crew Login
    echo -e "${BOLD}Crew Login Page${NC}\n"
    open_browser "http://localhost:5001/crew/login"
    
    run_test "Crew Login - Page Layout" \
             "Does page show centered card with ship icon and 'Crew Login' title?"
    
    run_test "Crew Login - Dropdown Functionality" \
             "Does the crew name dropdown show all crew members with large touch targets?"
    
    run_test "Crew Login - Password Toggle" \
             "Does the eye icon button toggle password visibility?"
    
    run_test "Crew Login - Successful Login" \
             "Can you log in successfully? (Use any crew name + password: crew67)"
    
    # Admin Login
    echo -e "${BOLD}Admin Login Page${NC}\n"
    open_browser "http://localhost:5001/admin/login"
    
    run_test "Admin Login - Page Layout" \
             "Does page show centered card with admin icon and 'Admin Login' title?"
    
    run_test "Admin Login - Password Toggle" \
             "Does the eye icon button toggle password visibility?"
    
    run_test "Admin Login - Successful Login" \
             "Can you log in successfully? (Username: admin, Password: admin67)"
}

# Admin Dashboard Tests
test_admin_dashboard() {
    print_section "📊 Admin Dashboard"
    
    echo -e "${CYAN}Ensure you're logged in as admin${NC}\n"
    open_browser "http://localhost:5001/admin/dashboard"
    
    run_test "Admin Dashboard - Card Grid Layout" \
             "Does the dashboard show cards in a responsive grid (3 cols desktop, 2 tablet, 1 mobile)?"
    
    run_test "Admin Dashboard - Status Badge Colors" \
             "Are status badges color-coded? (Blue=Submitted, Yellow=In Review, Red=Needs Revision, etc.)"
    
    run_test "Admin Dashboard - Filter Dropdown" \
             "Does the status filter dropdown work and filter work items?"
    
    run_test "Admin Dashboard - Search Functionality" \
             "Does the search box filter work items by item number/description?"
    
    run_test "Admin Dashboard - Batch Selection" \
             "Can you select multiple work items using checkboxes?"
    
    run_test "Admin Dashboard - Select All" \
             "Does the 'Select All' checkbox select/deselect all items?"
    
    run_test "Admin Dashboard - Download Batch" \
             "Does the 'Download Selected' button download a .zip file?"
}

# Photo Upload Tests
test_photo_upload() {
    print_section "📷 Photo Upload System"
    
    echo -e "${CYAN}Navigate to crew dashboard and create/edit a work item${NC}\n"
    
    run_test "Photo Upload - Drop Zone Display" \
             "Does the drop zone show with dashed border and upload icon?"
    
    echo -e "${YELLOW}Desktop Only:${NC} Try dragging an image file to the drop zone\n"
    run_test "Photo Upload - Drag & Drop" \
             "Does dragging and dropping an image file work? (Desktop only)"
    
    run_test "Photo Upload - Choose Photos Button" \
             "Does clicking 'Choose Photos' button open file picker?"
    
    run_test "Photo Upload - Instant Preview" \
             "After selecting a photo, does a preview appear within 1 second?"
    
    run_test "Photo Upload - Preview Card Details" \
             "Does preview card show thumbnail, filename, and file size?"
    
    run_test "Photo Upload - Caption Input" \
             "Can you type a caption for the photo?"
    
    run_test "Photo Upload - Delete Button" \
             "Does clicking the trash icon remove the photo smoothly?"
    
    run_test "Photo Upload - Multiple Photos" \
             "Can you upload multiple photos and see all previews?"
    
    run_test "Photo Upload - Max 10 Photos" \
             "Does the system prevent uploading more than 10 photos?"
    
    echo -e "${YELLOW}Try uploading a non-image file (e.g., .pdf)${NC}\n"
    run_test "Photo Upload - File Type Validation" \
             "Does uploading a non-image file show an error toast?"
}

# Crew Dashboard Tests
test_crew_dashboard() {
    print_section "📝 Crew Dashboard"
    
    echo -e "${CYAN}Ensure you're logged in as a crew member${NC}\n"
    open_browser "http://localhost:5001/crew/dashboard"
    
    run_test "Crew Dashboard - Tab Navigation" \
             "Can you switch between 'Submit New', 'In Progress', and 'Completed' tabs?"
    
    run_test "Crew Dashboard - Form Fields" \
             "Are all form fields visible and properly grouped?"
    
    run_test "Crew Dashboard - Form Submission" \
             "Can you submit a new work item successfully?"
    
    echo -e "${YELLOW}Note: Assigned items banner only shows if admin assigns an item back${NC}\n"
    run_test "Crew Dashboard - Assigned Items (if applicable)" \
             "If you have assigned items, does the banner show with revision notes?"
}

# Mobile Responsive Tests
test_mobile_responsive() {
    print_section "📱 Mobile Responsiveness"
    
    echo -e "${CYAN}Open browser DevTools and switch to responsive mode${NC}"
    echo -e "${CYAN}Test the following screen sizes:${NC}"
    echo -e "  - iPhone SE (320px)"
    echo -e "  - iPhone 12/13 (375px)"
    echo -e "  - iPad (768px)"
    echo -e "  - Desktop (1024px+)\n"
    
    read -p "$(echo -e ${YELLOW}Press Enter when DevTools is open...${NC})"
    
    run_test "Responsive - iPhone SE (320px)" \
             "At 320px width, do cards stack vertically and buttons remain tappable?"
    
    run_test "Responsive - iPhone 12/13 (375px)" \
             "At 375px width, does everything display without horizontal scroll?"
    
    run_test "Responsive - iPad (768px)" \
             "At 768px width, does admin dashboard show 2-column card grid?"
    
    run_test "Responsive - Desktop (1024px+)" \
             "At 1024px+ width, does admin dashboard show 3-column card grid?"
}

# Developer Console Tests
test_console() {
    print_section "🔧 Developer Console"
    
    echo -e "${CYAN}Open browser DevTools Console tab${NC}\n"
    
    run_test "Console - No JavaScript Errors" \
             "Are there any console errors or warnings on any page?"
    
    run_test "Console - Network Requests" \
             "In Network tab, do all CSS/JS/image files load successfully (200 status)?"
}

# Performance Tests
test_performance() {
    print_section "📈 Performance"
    
    run_test "Performance - Login Page Load Time" \
             "Does the login page load in under 2 seconds?"
    
    run_test "Performance - Dashboard Load Time" \
             "Does the dashboard load in under 3 seconds (with 10+ items)?"
    
    run_test "Performance - Photo Preview Speed" \
             "Does photo preview appear in under 1 second?"
}

# Generate summary
generate_summary() {
    print_section "✅ Test Summary"
    
    echo -e "${BOLD}Total Tests Run:${NC} ${TOTAL_TESTS}"
    echo -e "${GREEN}${BOLD}Passed:${NC} ${PASSED_TESTS}"
    echo -e "${RED}${BOLD}Failed:${NC} ${FAILED_TESTS}"
    echo -e "${YELLOW}${BOLD}Skipped:${NC} ${SKIPPED_TESTS}"
    
    # Calculate pass rate
    if [ $TOTAL_TESTS -gt 0 ]; then
        PASS_RATE=$(awk "BEGIN {printf \"%.1f\", ($PASSED_TESTS/$TOTAL_TESTS)*100}")
        echo -e "\n${BOLD}Pass Rate:${NC} ${PASS_RATE}%"
    fi
    
    # Show failed tests
    if [ ${#FAILED_TEST_NAMES[@]} -gt 0 ]; then
        echo -e "\n${RED}${BOLD}Failed Tests:${NC}"
        for test in "${FAILED_TEST_NAMES[@]}"; do
            echo -e "  ${RED}✗${NC} $test"
        done
    fi
    
    # Recommendation
    echo -e "\n${BOLD}Recommendation:${NC}"
    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "${GREEN}${BOLD}✓ APPROVED${NC} - Ready to merge to main!"
    elif [ $FAILED_TESTS -le 2 ]; then
        echo -e "${YELLOW}${BOLD}⚠ APPROVED WITH MINOR FIXES${NC} - Address minor issues then merge"
    else
        echo -e "${RED}${BOLD}✗ REQUIRES FIXES${NC} - Address issues before merging"
    fi
    
    # Save results to file
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    RESULTS_FILE="test_results_${TIMESTAMP}.txt"
    
    {
        echo "Frontend Modernization Test Results - PR #1"
        echo "Date: $(date)"
        echo "=========================================="
        echo ""
        echo "Total Tests: $TOTAL_TESTS"
        echo "Passed: $PASSED_TESTS"
        echo "Failed: $FAILED_TESTS"
        echo "Skipped: $SKIPPED_TESTS"
        echo "Pass Rate: ${PASS_RATE}%"
        echo ""
        if [ ${#FAILED_TEST_NAMES[@]} -gt 0 ]; then
            echo "Failed Tests:"
            for test in "${FAILED_TEST_NAMES[@]}"; do
                echo "  - $test"
            done
        fi
    } > "$RESULTS_FILE"
    
    echo -e "\n${CYAN}Results saved to: ${RESULTS_FILE}${NC}"
}

# Cleanup
cleanup() {
    echo -e "\n${CYAN}Cleaning up...${NC}"
    
    if [ ! -z "$SERVER_PID" ]; then
        read -p "$(echo -e ${YELLOW}Stop the test server? [y/n]: ${NC})" stop_server
        if [[ $stop_server =~ ^[Yy]$ ]]; then
            echo -e "${CYAN}Stopping server (PID: ${SERVER_PID})...${NC}"
            kill $SERVER_PID 2>/dev/null
            echo -e "${GREEN}Server stopped${NC}"
        else
            echo -e "${YELLOW}Server left running on port 5001${NC}"
        fi
    fi
    
    echo -e "${GREEN}${BOLD}Testing complete!${NC}"
}

# Main execution
main() {
    # Trap Ctrl+C
    trap cleanup EXIT
    
    print_banner
    
    echo -e "${CYAN}This script will guide you through testing the frontend modernization.${NC}"
    echo -e "${CYAN}You'll be prompted to test features and mark them as pass/fail.${NC}\n"
    
    read -p "$(echo -e ${YELLOW}Ready to begin? [y/n]: ${NC})" ready
    if [[ ! $ready =~ ^[Yy]$ ]]; then
        echo -e "${RED}Testing cancelled.${NC}"
        exit 0
    fi
    
    # Start server
    start_server
    
    # Run test suites
    test_critical_bugs
    test_login_pages
    test_admin_dashboard
    test_photo_upload
    test_crew_dashboard
    test_mobile_responsive
    test_console
    test_performance
    
    # Generate summary
    generate_summary
}

# Run main
main

