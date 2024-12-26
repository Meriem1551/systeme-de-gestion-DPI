import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-patient-selection',
  imports: [CommonModule],
  templateUrl: './patient-selection.component.html',
  styleUrls: ['./patient-selection.component.css']
})
export class PatientSelectionComponent {
  @Output() patientSelected = new EventEmitter<number>(); // Emit the selected patient's ID

  patients = [
    { id: 1, name: 'agal imene' },
    { id: 2, name: 'bouderbala amira' },
    { id: 3, name: 'djerfi fatma' }
  ]; // Mock list of patients

  onPatientChange(event: Event): void {
    const selectElement = event.target as HTMLSelectElement;
    const selectedPatientId = Number(selectElement.value);
    this.patientSelected.emit(selectedPatientId); // Emit the selected patient ID
  }
}
