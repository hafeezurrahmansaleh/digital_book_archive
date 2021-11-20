import React from 'react';
import { Container } from 'react-bootstrap';

const Footer = () => {
    return (
        <Container>
            <footer>
                <small>
                    © {new Date().getFullYear()} made by Subroto Karmokar
                </small>
            </footer>
        </Container>
    );
};

export default Footer;