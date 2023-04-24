import React, { useState } from 'react';
import MainNavigation from './MainNavigation';
import SideNavigation from './SideNavigation';
import classes from './Layout.module.css';
function Layout({children}) {
    const [navbarOpen, setNavbarOpen] = useState(false)
    function toggleHandler() {
        setNavbarOpen(!navbarOpen);
    }
    return(
        <div>
            <MainNavigation toggleHandler={toggleHandler}/>
            {navbarOpen && <SideNavigation />}
            <main className={classes.main}>
                {children}
            </main>
        </div>
    );
}
export default Layout;