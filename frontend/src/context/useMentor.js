import { useContext } from 'react';
import { MentorContext } from './MentorContext';

export function useMentor() {
  const context = useContext(MentorContext);
  if (!context) throw new Error('useMentor must be used within a MentorProvider');
  return context;
}
