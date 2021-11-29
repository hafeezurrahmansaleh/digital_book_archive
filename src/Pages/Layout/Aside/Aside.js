import React from 'react';
import {
    ProSidebar,
    Menu,
    MenuItem,
    SidebarHeader,
    SidebarFooter,
    SidebarContent,
} from 'react-pro-sidebar';
import { FaUserAlt, FaBook, FaBuilding, FaUserCheck, FaTasks, FaCreditCard, FaUserShield, FaSignOutAlt } from 'react-icons/fa';
import { Button } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import useAuth from '../../../hooks/useAuth';

const activeStyle = {
    fontWeight: "bold",
    fontSize: "16px",
    color: "#8270C1",
    backgroundColor: 'white',
    padding: '0 5px 1px 5px',
    borderRadius: '15px'
}

const Aside = ({ url, collapsed, toggled, handleToggleSidebar }) => {
    const { user, logoutUser } = useAuth()
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
                    Admin Dashboard
                </div>
            </SidebarHeader>

            <SidebarContent>
                <Menu iconShape="circle">
                    {user.is_superuser && <MenuItem icon={<FaUserShield />}><a href="http://127.0.0.1:8000/admin/"> Super Admin</a></MenuItem>}
                    <MenuItem icon={<FaTasks />}><NavLink activeStyle={activeStyle} exact to={`${url}`}> Summary</NavLink></MenuItem>
                </Menu>
                <SidebarHeader>
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
                    All Reports
                </div>
                </SidebarHeader>
                <Menu iconShape="circle">
                    <MenuItem icon={<FaUserAlt />}><NavLink activeStyle={activeStyle} to={`${url}/customers`}> Customers</NavLink></MenuItem>
                    <MenuItem icon={<FaBook />}><NavLink activeStyle={activeStyle} to={`${url}/books`}> Books</NavLink></MenuItem>
                    <MenuItem icon={<FaBuilding />}><NavLink activeStyle={activeStyle} to={`${url}/publishers`}> Publishers</NavLink></MenuItem>
                    <MenuItem icon={<FaUserCheck />}><NavLink activeStyle={activeStyle} to={`${url}/subscriptions`}> Subscriptions</NavLink></MenuItem>
                    <MenuItem icon={<FaCreditCard />}><NavLink activeStyle={activeStyle} to={`${url}/transactions`}> Transactions</NavLink></MenuItem>
                </Menu>
            </SidebarContent>

            <SidebarFooter style={{ textAlign: 'center' }}>
                <div
                    className="sidebar-btn-wrapper"
                    style={{
                        padding: '20px 24px',
                    }}
                >
                    <Button varient="light" onClick={logoutUser} className="sidebar-btn"><FaSignOutAlt className="me-2" /> Logout</Button>
                </div>
            </SidebarFooter>
        </ProSidebar>
    );
};

export default Aside;
