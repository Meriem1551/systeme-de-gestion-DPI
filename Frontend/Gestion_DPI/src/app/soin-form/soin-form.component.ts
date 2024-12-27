import { Component, Input, Output, EventEmitter } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-soin-form',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './soin-form.component.html',
  styleUrls: ['./soin-form.component.css']
})
export class SoinFormComponent {
  @Input() index!: number; // Index du formulaire
  @Output() delete = new EventEmitter<void>(); // Événement pour supprimer le formulaire
  @Output() soinDataChanged = new EventEmitter<{ description: string, observation: string }>();

  description: string = '';
  observation: string = '';

  // Méthode appelée lorsqu'un champ est modifié
  onInputChange(): void {
    this.soinDataChanged.emit({
      description: this.description,
      observation: this.observation
    });
  }

  // Méthode pour supprimer un formulaire
  onDelete(): void {
    this.delete.emit();
  }
}
