import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogContent , MatDialogActions, MatDialogClose , MatDialogTitle, MatDialogContainer  } from '@angular/material/dialog';

@Component({
  selector: 'app-resume',
  imports: [MatDialogContent ,
              MatDialogActions,
              MatDialogClose , 
              MatDialogTitle ,
              CommonModule,
              MatDialogContainer],
  templateUrl: './resume.component.html',
  styleUrl: './resume.component.css'
})
export class ResumeComponent {
  Symptomes = "Symptomes";
  Diagnostic="Diagnostic";
  Antecedents="Antécédents";
  autres="autres";
}
