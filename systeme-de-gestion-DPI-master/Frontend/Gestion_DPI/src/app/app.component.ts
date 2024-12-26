import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { CreationDPIComponent } from './creation-dpi/creation-dpi.component';
@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CreationDPIComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
}
