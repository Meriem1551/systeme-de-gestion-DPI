import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreationConsultationComponent } from './creation-consultation.component';

describe('CreationConsultationComponent', () => {
  let component: CreationConsultationComponent;
  let fixture: ComponentFixture<CreationConsultationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreationConsultationComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreationConsultationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
