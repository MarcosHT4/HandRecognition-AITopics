import React from 'react';
import {Typography} from "@mui/material";
import example from "../images/example.jpeg";

const Description = () => {
    return (
        <section className="description">
            <Typography
                variant="h5"
                component="a"
                sx={{
                    mr: 2,
                    display: { xs: 'none', md: 'flex' },
                    fontFamily: 'monospace',
                    fontWeight: 700,
                    letterSpacing: '.3rem',
                    color: 'inherit',
                    textDecoration: 'none',
                    textAlign: 'center',
                }}
            >
                Transform images instantly with our Hand Detector AI. Upload, analyze, and unlock a new realm of
                possibilities in VR, AR, and beyond. Elevate your user experience effortlessly!
            </Typography>
            <Typography
                variant="h6"
                component="a"
                sx={{
                    mr: 2,
                    display: { xs: 'none', md: 'flex' },
                    fontFamily: 'monospace',
                    fontWeight: 700,
                    letterSpacing: '.3rem',
                    color: 'inherit',
                    textDecoration: 'none',
                    textAlign: 'center',
                }}
            >
                Upload an image with a maximum of two hands, and see the magic happen!
                Our AI model will detect the hands, and draw landmarks on the most important parts of the hands.
            </Typography>


        </section>
    );
};

export default Description;