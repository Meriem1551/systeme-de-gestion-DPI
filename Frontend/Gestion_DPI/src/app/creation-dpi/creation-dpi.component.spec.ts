import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreationDPIComponent } from './creation-dpi.component';

describe('CreationDPIComponent', () => {
  let component: CreationDPIComponent;
  let fixture: ComponentFixture<CreationDPIComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreationDPIComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreationDPIComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
