import React from 'react';
import { motion, useReducedMotion } from 'framer-motion';

export default function AnimatedPage({ children, className = '' }) {
  const shouldReduceMotion = useReducedMotion();

  const variants = {
    initial: shouldReduceMotion
      ? { opacity: 0 }
      : { opacity: 0, x: 20 },
    animate: shouldReduceMotion
      ? { opacity: 1 }
      : { opacity: 1, x: 0 },
    exit: shouldReduceMotion
      ? { opacity: 0 }
      : { opacity: 0, x: -20 },
  };

  const transition = shouldReduceMotion
    ? { duration: 0.05 }
    : { duration: 0.32, ease: [0.25, 0.1, 0.25, 1.0] };

  return (
    <motion.div
      variants={variants}
      initial="initial"
      animate="animate"
      exit="exit"
      transition={transition}
      className={`page-container ${className}`}
    >
      {children}
    </motion.div>
  );
}
