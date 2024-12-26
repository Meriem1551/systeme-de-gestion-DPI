import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecherchePatientComponent } from './recherche-patient.component';

describe('RecherchePatientComponent', () => {
  let component: RecherchePatientComponent;
  let fixture: ComponentFixture<RecherchePatientComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RecherchePatientComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RecherchePatientComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
