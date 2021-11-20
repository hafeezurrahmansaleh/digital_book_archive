import React from 'react';
import {
    ProSidebar,
    Menu,
    MenuItem,
    SubMenu,
    SidebarHeader,
    SidebarFooter,
    SidebarContent,
} from 'react-pro-sidebar';
import { FaTachometerAlt, FaGem, FaList, FaGithub, FaRegLaughWink, FaHeart, FaUserAlt, FaBook, FaBuilding, FaUserCheck, FaTasks } from 'react-icons/fa';
import sidebarBg from '../../../assets/bg2.jpg';
import { Button } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';

const activeStyle = {
    fontWeight: "bold",
    fontSize: "16px",
    color: "#dee2ec",
}

const Aside = ({ url, collapsed, toggled, handleToggleSidebar }) => {
    return (
        <ProSidebar
            // image={image ? sidebarBg : false}
            collapsed={collapsed}
            toggled={toggled}
            breakPoint="md"
            onToggle={handleToggleSidebar}
        >
            <SidebarHeader>
                <div
                    style={{
                        padding: '24px',
                        textTransform: 'uppercase',
                        fontWeight: 'bold',
                        fontSize: 14,
                        letterSpacing: '1px',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                    }}
                >
                    Admin
                </div>
            </SidebarHeader>

            <SidebarContent>
                <Menu iconShape="circle">
                    <MenuItem icon={<FaTasks />}><NavLink activeStyle={activeStyle} exact to={`${url}`}> Summary</NavLink></MenuItem>
                </Menu>
                <div
                    style={{
                        padding: '7px 24px',
                        textTransform: 'uppercase',
                        fontWeight: 'bold',
                        fontSize: 14,
                        letterSpacing: '1px',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                    }}
                >
                    Reports
                </div>
                <Menu iconShape="circle">
                    <MenuItem icon={<FaUserAlt />}><NavLink activeStyle={activeStyle} to={`${url}/customers`}> Customers</NavLink></MenuItem>
                    <MenuItem icon={<FaBook />}><NavLink activeStyle={activeStyle} to={`${url}/books`}> Books</NavLink></MenuItem>
                    <MenuItem icon={<FaBuilding />}><NavLink activeStyle={activeStyle} to={`${url}/publishers`}> Publishers</NavLink></MenuItem>
                    <MenuItem icon={<FaUserCheck />}><NavLink activeStyle={activeStyle} to={`${url}/subscriptions`}> Subscriptions</NavLink></MenuItem>
                </Menu>
            </SidebarContent>

            <SidebarFooter style={{ textAlign: 'center' }}>
                <div
                    className="sidebar-btn-wrapper"
                    style={{
                        padding: '20px 24px',
                    }}
                >
                    <Button varient="light" className="sidebar-btn">Logout</Button>
                </div>
            </SidebarFooter>
        </ProSidebar>
    );
};

export default Aside;
