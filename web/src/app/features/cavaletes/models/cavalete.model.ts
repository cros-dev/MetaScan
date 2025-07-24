import {Slot} from './slot.model';

export interface Cavalete {
  id: number;
  code: string;
  name: string;
  user: string | null;
  status: string;
  slots: Slot[];
  occupancy: string;
}
