import React from 'react';
import { motion, useReducedMotion } from 'framer-motion';

export default function AnimatedPage({ children, className = '' }) {
  const reduceMotion = useReducedMotion();
  return (
    <motion.div
      className={`page-container ${className}`}
      initial={reduceMotion ? { opacity: 0 } : { opacity: 0, x: 16 }}
      animate={{ opacity: 1, x: 0 }}
      exit={reduceMotion ? { opacity: 0 } : { opacity: 0, x: -16 }}
      transition={{ duration: reduceMotion ? 0 : 0.24 }}
    >
      {children}
    </motion.div>
  );
}
